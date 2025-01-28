import asyncio
import json
import logging
import os
import socket
import threading
import uuid
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Any, Callable, Dict, List, Optional, TypeVar, Union, Tuple
from urllib.parse import urlparse

import websockets
from gentrace.api_client import ApiClient
from gentrace.apis.tags.v1_api import V1Api
from gentrace.configuration import Configuration
from gentrace.providers.init import (
    GENTRACE_CONFIG_STATE,
)
from gentrace.providers.pipeline import Pipeline
from gentrace.providers.utils import log_debug, log_info, log_warn
import pystache
from gentrace.providers.evaluation import update_test_result_with_runners
from websockets.client import connect as ws_connect
from asyncio import Semaphore
import requests

T = TypeVar("T")

# Context management for overrides
overrides_context: ContextVar[Dict[str, Any]] = ContextVar("overrides", default={})

@contextmanager
def override_context(overrides: Dict[str, Any]):
    """Context manager for handling overrides during test execution."""
    token = overrides_context.set(overrides)
    try:
        yield
    finally:
        overrides_context.reset(token)

def get_value(name: str, default_value: T) -> T:
    """Get a value from the current context or return default."""
    overrides = overrides_context.get()
    value = overrides.get(name, default_value)
    return value

# Global state for interactions and test suites
interactions: Dict[str, Dict] = {}
test_suites: Dict[str, Dict] = {}
listeners: Dict[str, Callable] = {}

def define_interaction(interaction: Dict) -> Callable:
    """Define a new interaction for testing."""
    interactions[interaction["name"]] = interaction
    for listener in listeners.values():
        listener({
            "type": "register-interaction",
            "interaction": interaction
        })
    return interaction["fn"]

def define_test_suite(test_suite: Dict) -> Callable:
    """Define a new test suite."""
    test_suites[test_suite["name"]] = test_suite
    for listener in listeners.values():
        listener({
            "type": "register-test-suite",
            "test_suite": test_suite
        })
    return test_suite["fn"]

def template_parameter(config: Dict[str, Any]) -> Dict[str, Any]:
    """Create a template parameter."""
    return {
        "name": config["name"],
        "type": "template",
        "defaultValue": config["defaultValue"],
        "variables": config.get("variables", []),
        "render": lambda values: pystache.render(get_value(config["name"], config["defaultValue"]), values)
    }

def numeric_parameter(config: Dict[str, Any]) -> Dict[str, Any]:
    """Create a numeric parameter."""
    return {
        "name": config["name"],
        "type": "numeric",
        "defaultValue": config["defaultValue"],
        "getValue": lambda: get_value(config["name"], config["defaultValue"])
    }

def enum_parameter(config: Dict[str, Any]) -> Dict[str, Any]:
    """Create an enum parameter."""
    return {
        "name": config["name"],
        "type": "enum",
        "defaultValue": config["defaultValue"],
        "options": config["options"],
        "getValue": lambda: get_value(config["name"], config["defaultValue"])
    }

def string_parameter(config: Dict[str, Any]) -> Dict[str, Any]:
    """Create a string parameter."""
    return {
        "name": config["name"],
        "type": "string",
        "defaultValue": config["defaultValue"],
        "getValue": lambda: get_value(config["name"], config["defaultValue"])
    }

def get_ws_base_path() -> str:
    """Get the WebSocket base path based on configuration."""
    if not GENTRACE_CONFIG_STATE["global_gentrace_config"]:
        return "wss://gentrace.ai/ws"
    
    parsed = urlparse(GENTRACE_CONFIG_STATE["global_gentrace_config"].host)
    if "localhost" in parsed.netloc:
        return "ws://localhost:3001"
    
    base_path = f"wss://{parsed.netloc}/ws"
    return base_path

async def handle_message(message: Dict, transport: Dict) -> None:
    """Handle incoming WebSocket messages."""
    message_type = message.get("type")
    print(f"Received message type: {message_type}")
    
    if message_type == "environment-details":
        print("Processing environment details request")
        await send_message({
            "type": "environment-details",
            "interactions": [
                {
                    "name": interaction["name"],
                    "hasValidation": bool(interaction.get("inputType")),
                    "parameters": interaction.get("parameters", [])
                }
                for interaction in interactions.values()
            ],
            "testSuites": [
                {"name": suite["name"]}
                for suite in test_suites.values()
            ]
        }, transport)
    
    elif message_type == "run-interaction-input-validation":
        print(f"Running input validation for interaction: {message['interactionName']}")
        interaction = interactions.get(message["interactionName"])
        if not interaction:
            await send_message({
                "type": "run-interaction-input-validation-results",
                "id": message["id"],
                "interactionName": message["interactionName"],
                "data": [
                    {
                        "id": tc["id"],
                        "status": "failure",
                        "error": f"Interaction {message['interactionName']} not found"
                    }
                    for tc in message["data"]
                ]
            }, transport)
            return

        results = []
        for test_case in message["data"]:
            try:
                if interaction.get("inputType"):
                    await interaction["inputType"].parse_obj(test_case["inputs"])
                    results.append({"id": test_case["id"], "status": "success"})
                else:
                    results.append({
                        "id": test_case["id"],
                        "status": "failure",
                        "error": "No input validator found"
                    })
            except Exception as e:
                results.append({
                    "id": test_case["id"],
                    "status": "failure",
                    "error": str(e)
                })
        
        await send_message({
            "type": "run-interaction-input-validation-results",
            "id": message["id"],
            "interactionName": message["interactionName"],
            "data": results
        }, transport)

    elif message_type == "run-test-interaction":
        print(f"Running test interaction: {message['interactionName']}")
        await send_message({"type": "confirmation", "ok": True}, transport)
        
        pipeline = Pipeline({"id": message["pipelineId"]})
        interaction = interactions.get(message["interactionName"])
        
        if not interaction:
            log_warn(f"Interaction {message['interactionName']} not found")
            return
            
        with override_context(message.get("overrides", {})):
            # Get parallelism from message, default to 1 if not specified
            parallelism = message.get("parallelism", 1)
            semaphore = Semaphore(parallelism)
            
            async def run_with_semaphore(test_case: Dict):
                async with semaphore:
                    return await run_test_case_through_interaction(pipeline, interaction, test_case)
            
            # Run all test cases in parallel with semaphore control
            try:
                results = await asyncio.gather(
                    *[run_with_semaphore(test_case) for test_case in message["data"]],
                    return_exceptions=True
                )
                print(f"Completed test cases execution with {len(results)} results")
                
                # Process results and update test results
                error_results = []
                for result in results:
                    if isinstance(result, Exception):
                        log_warn(f"Error in parallel execution: {result}")
                        error_results.append(str(result))
                        continue
                    runner, test_case = result
                    update_test_result_with_runners(message["testJobId"], [(runner, test_case)])
                
                # Send final status update
                if not GENTRACE_CONFIG_STATE["global_gentrace_config"]:
                    raise ValueError("Gentrace configuration not initialized")
                
                config = GENTRACE_CONFIG_STATE["global_gentrace_config"]
                host = config.host or "https://gentrace.ai/api"
                
               
                # Get auth settings from config
                auth_settings = config.auth_settings()
                
                # Prepare headers from config with auth
                headers = {
                    "Content-Type": "application/json",
                }
                
                # Add bearer token if available
                if 'bearerAuth' in auth_settings:
                    headers[auth_settings['bearerAuth']['key']] = auth_settings['bearerAuth']['value']
                
                # Make status update request
                status_url = f"{host}/v1/test-result/status"
                status_payload = {
                    "id": message["testJobId"],
                    "finished": True
                }
                
                response = requests.post(
                    status_url,
                    headers=headers,
                    json=status_payload
                )
                
                if not response.ok:
                    log_warn(f"Failed to update test status: {response.text}")
            except Exception as e:
                log_warn(f"Error in parallel test execution: {e}")

    elif message_type == "run-test-suite":
        print(f"Running test suite: {message['testSuiteName']}")
        test_suite = test_suites.get(message["testSuiteName"])
        if not test_suite:
            log_warn(f"Test suite {message['testSuiteName']} not found")
            return
            
        try:
            await test_suite["fn"]()
            await update_test_status(message["testJobId"], True)
        except Exception as e:
            await update_test_status(message["testJobId"], True, str(e))

async def send_message(message: Dict, transport: Dict) -> None:
    """Send a message through the WebSocket transport."""
    if transport["type"] == "ws":
        if not transport.get("pluginId"):
            transport["messageQueue"].append(message)
            return
            
        if transport.get("isClosed"):
            return
            
        await transport["ws"].send(json.dumps({
            "id": str(uuid.uuid4()),
            "for": transport["pluginId"],
            "data": message
        }))
    else:
        transport["sendResponse"](message)


async def update_test_status(test_job_id: str, finished: bool, error: Optional[str] = None) -> None:
    """Update test job status in the Gentrace API."""
    if not GENTRACE_CONFIG_STATE["global_gentrace_config"]:
        raise ValueError("Gentrace configuration not initialized")
        
    api_client = ApiClient(configuration=GENTRACE_CONFIG_STATE["global_gentrace_config"])
    api = V1Api(api_client=api_client)
    
    await api.v1_test_result_status_post({
        "id": test_job_id,
        "finished": finished,
        "error": error
    })

async def run_websocket(environment_name: Optional[str] = None) -> None:
    """Run the WebSocket connection to the Gentrace server."""
    if not GENTRACE_CONFIG_STATE["GENTRACE_API_KEY"]:
        raise ValueError("Gentrace API key not set")
    
    ws_base_path = get_ws_base_path()
    env = environment_name or GENTRACE_CONFIG_STATE.get("GENTRACE_ENVIRONMENT_NAME") or socket.gethostname()
    
    transport = {
        "type": "ws",
        "pluginId": None,
        "messageQueue": [],
        "isClosed": False
    }

    async def setup():
        """Setup function to register existing interactions and test suites."""
        # Register existing interactions
        for interaction in interactions.values():
            parameters = []
            for param in interaction.get("parameters", []):
                param_copy = param.copy()
                # Remove any function properties
                param_copy.pop("render", None)  # For template parameters
                param_copy.pop("getValue", None)  # For numeric/enum parameters
                parameters.append(param_copy)
            
            await send_message({
                "type": "register-interaction",
                "interaction": {
                    "name": interaction["name"],
                    "hasValidation": bool(interaction.get("inputType")),
                    "parameters": parameters
                }
            }, transport)
        
        # Register existing test suites
        for test_suite in test_suites.values():
            await send_message({
                "type": "register-test-suite",
                "testSuite": {
                    "name": test_suite["name"]
                }
            }, transport)

    websocket = await ws_connect(ws_base_path)
    transport["ws"] = websocket
    
    try:
        print("WebSocket connection opened, sending setup message")
        setup_message = {
            "id": str(uuid.uuid4()),
            "init": "test-job-runner", 
            "data": {
                "type": "setup",
                "environmentName": env,
                "apiKey": GENTRACE_CONFIG_STATE["GENTRACE_API_KEY"]
            }
        }
        await websocket.send(json.dumps(setup_message))

        # Start ping and heartbeat tasks
        async def send_ping():
            while not transport["isClosed"]:
                try:
                    print("sending ping")
                    await websocket.send(json.dumps({
                        "id": str(uuid.uuid4()),
                        "ping": True
                    }))
                    await asyncio.sleep(30)  # 30 seconds interval
                except Exception as e:
                    if not transport["isClosed"]:
                        break

        async def send_heartbeat():
            while not transport["isClosed"]:
                try:
                    print("sending heartbeat")
                    await send_message({
                        "type": "heartbeat"
                    }, transport)
                    await asyncio.sleep(30)  # 30 seconds interval
                except Exception as e:
                    if not transport["isClosed"]:
                        break

        ping_task = asyncio.create_task(send_ping())
        heartbeat_task = asyncio.create_task(send_heartbeat())

        try:
            while True:
                message = await websocket.recv()
                message_data = json.loads(message)
                print("WebSocket message received:", message)
                
                if "pluginId" in message_data.get("data", {}):
                    transport["pluginId"] = message_data["data"]["pluginId"]
                    # Process queued messages and setup registrations
                    for queued_message in transport["messageQueue"]:
                        await send_message(queued_message, transport)
                    transport["messageQueue"].clear()
                    await setup()  # Register existing interactions and test suites
                    continue

                if message_data.get("error"):
                    log_warn(f"WebSocket error: {message_data['error']}")
                    continue
                    
                try:
                    await handle_message(message_data["data"], transport)
                except Exception as e:
                    log_warn(f"Error handling message: {e}")
                    
        except websockets.exceptions.ConnectionClosed:
            print("WebSocket connection closed")
            transport["isClosed"] = True
        except Exception as e:
            print(f"Error in WebSocket message handler: {e}")
            transport["isClosed"] = True
        finally:
            transport["isClosed"] = True
            ping_task.cancel()
            heartbeat_task.cancel()
            try:
                await asyncio.gather(ping_task, heartbeat_task, return_exceptions=True)
            except asyncio.CancelledError:
                pass
    finally:
        await websocket.close()

async def listen_inner(environment_name: Optional[str] = None, retries: int = 0) -> None:
    """Internal function to handle WebSocket connection with retries."""
    if not GENTRACE_CONFIG_STATE["GENTRACE_API_KEY"]:
        raise ValueError("Gentrace API key not set")
        
    try:
        await run_websocket(environment_name)
    except Exception as e:
        if retries < 5:  # Max 5 retries
            await asyncio.sleep(min(2 ** retries * 0.25, 10))
            await listen_inner(environment_name, retries + 1)
        else:
            raise

def listen(environment_name: Optional[str] = None) -> None:
    """Start listening for test jobs from the Gentrace server."""
    asyncio.run(listen_inner(environment_name))

async def handle_webhook(body: Dict, send_response: Optional[Callable[[Dict], None]] = None) -> Dict:
    """
    Handle webhook requests for test job execution.
    
    Args:
        body: The webhook request body
        send_response: Optional callback function to send response back to the webhook caller
    
    Returns:
        Dict containing the response data
    """
    print("Gentrace HTTP message received:", body)
    
    response_data = {}
    
    # Create an HTTP transport for webhook communication
    transport = {
        "type": "http",
        "sendResponse": send_response if send_response else lambda x: response_data.update(x)
    }
    
    try:
        # Process the webhook message using the existing message handler
        await handle_message(body, transport)
        
        # If no send_response provided, return the collected response
        if not send_response:
            return response_data
            
    except Exception as e:
        error_response = {
            "type": "error",
            "error": str(e)
        }
        
        # If send_response provided, use it, otherwise return error
        if send_response:
            send_response(error_response)
        return error_response

async def run_test_case_through_interaction(pipeline: Pipeline, interaction: Dict, test_case: Dict) -> Tuple[Any, Dict]:
    """Run a single test case through an interaction and return the runner and test case."""
    print(f"Running test case {test_case['id']}")
    runner = pipeline.start()
    try:
        await runner.ameasure(interaction["fn"], inputs=test_case["inputs"])
        print(f"Successfully completed test case {test_case['id']}")
    except Exception as e:
        print(f"Failed to run test case {test_case['id']}: {str(e)}")
        runner.set_error(str(e))
    return runner, test_case
