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

T = TypeVar("T")

logger = logging.getLogger(__name__)

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
        "render": lambda values: pystache.render(config["defaultValue"], values)
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
    print("WebSocket message received:", message)
    message_type = message.get("type")
    
    if message_type == "environment-details":
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
        await send_message({"type": "confirmation", "ok": True}, transport)
        
        pipeline = Pipeline({"id": message["pipelineId"]})
        interaction = interactions.get(message["interactionName"])
        
        if not interaction:
            log_warn(f"Interaction {message['interactionName']} not found")
            return
            
        with override_context(message.get("overrides", {})):
            for test_case in message["data"]:
                try:
                    runner = pipeline.start()
                    await runner.ameasure(interaction["fn"], inputs=test_case["inputs"])
                    update_test_result_with_runners(message["testJobId"], [(runner, test_case)])
                except Exception as e:
                    log_warn(f"Error running test case {test_case['id']}: {e}")
                    runner.set_error(str(e))
                    update_test_result_with_runners(message["testJobId"], [(runner, test_case)])

    elif message_type == "run-test-suite":
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
            
        print("WebSocket sending message:", json.dumps(message, indent=2))
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
    
    async with websockets.connect(ws_base_path) as websocket:
        transport["ws"] = websocket
        
        print("WebSocket connection opened, sending setup message")
        # Send initial setup message
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

        # Start ping task
        async def send_ping():
            while not transport["isClosed"]:
                try:
                    print("Sending ping")
                    await websocket.send(json.dumps({
                        "id": str(uuid.uuid4()),
                        "ping": True
                    }))
                    await asyncio.sleep(30)  # 30 seconds interval
                except Exception as e:
                    if not transport["isClosed"]:
                        break

        ping_task = asyncio.create_task(send_ping())
        
        try:
            while True:
                message = await websocket.recv()
                message_data = json.loads(message)
                
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
            transport["isClosed"] = True
            print("WebSocket connection closed")
        except Exception as e:
            transport["isClosed"] = True
            print(f"WebSocket error: {e}")
        finally:
            transport["isClosed"] = True
            ping_task.cancel()
            try:
                await ping_task
            except asyncio.CancelledError:
                pass

async def listen_inner(environment_name: Optional[str] = None, retries: int = 0) -> None:
    """Internal function to handle WebSocket connection with retries."""
    if not GENTRACE_CONFIG_STATE["GENTRACE_API_KEY"]:
        raise ValueError("Gentrace API key not set")
        
    try:
        await run_websocket(environment_name)
    except Exception as e:
        print(f"Error in WebSocket connection: {e}")
        if retries < 5:  # Max 5 retries
            await asyncio.sleep(min(2 ** retries * 0.25, 10))
            await listen_inner(environment_name, retries + 1)
        else:
            raise

def listen(environment_name: Optional[str] = None) -> None:
    """Start listening for test jobs from the Gentrace server."""
    asyncio.run(listen_inner(environment_name))

async def handle_webhook(body: Dict, send_response: Callable[[Dict], None]) -> None:
    """Handle webhook requests for test job execution."""
    print("Gentrace HTTP message received:", json.dumps(body, indent=2))
    await handle_message(body, {
        "type": "http",
        "sendResponse": send_response
    })
