import os
from typing import Any, Dict

# Set OTEL environment variables first
os.environ['LANGSMITH_OTEL_ENABLED'] = 'true'
os.environ['LANGSMITH_OTEL_ONLY'] = 'true'
os.environ['LANGSMITH_TRACING'] = 'true'

from langgraph.prebuilt import create_react_agent  # type: ignore[import]
from langchain_core.tools import tool  # type: ignore[import]

from gentrace import init, interaction

init()

@tool
def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

@interaction(name="math-agent-interaction")
def run_math_agent() -> Dict[str, Any]:
    math_agent = create_react_agent(  # type: ignore[var-annotated]
        'openai:gpt-4o',
        tools=[add],
        name='math_agent'
    )

    result: Dict[str, Any] = math_agent.invoke({  # type: ignore[attr-defined]
        'messages': [{
            'role': 'user',
            'content': "What's 123 + 456?"
        }]
    })
    
    return result

if __name__ == "__main__":
    result = run_math_agent()
    print(result)
