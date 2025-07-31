import os
from typing import Any, Dict

# Set OTEL environment variables first
os.environ['LANGSMITH_OTEL_ENABLED'] = 'true'
os.environ['LANGSMITH_OTEL_ONLY'] = 'true'
os.environ['LANGSMITH_TRACING'] = 'true'

from langgraph.prebuilt import create_react_agent  # type: ignore[import]
from langchain_core.tools import tool  # type: ignore[import]

import gentrace
from gentrace import interaction

# Initialize Gentrace
gentrace.init(api_key=os.getenv("GENTRACE_API_KEY"))

# Define a tool for the agent
@tool
def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

# Create the agent wrapped in a Gentrace interaction
@interaction(name="math-agent-interaction")
def run_math_agent() -> Dict[str, Any]:
    # Create a ReAct agent with the add tool
    math_agent = create_react_agent(  # type: ignore[var-annotated]
        'openai:gpt-4o',
        tools=[add],
        name='math_agent'
    )
    
    # Invoke the agent
    result: Dict[str, Any] = math_agent.invoke({  # type: ignore[attr-defined]
        'messages': [{
            'role': 'user',
            'content': "What's 123 + 456?"
        }]
    })
    
    return result

# Run the traced agent
if __name__ == "__main__":
    result = run_math_agent()
    print(result)
