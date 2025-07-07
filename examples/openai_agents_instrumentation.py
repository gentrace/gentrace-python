"""
OpenAI Agents instrumentation example using OpenInference with Gentrace.

Shows how to instrument OpenAI Agents SDK with automatic tracing of:
- Agent conversations and tool calls
- Agent handoffs between specialized agents
- Full observability through Gentrace
"""

import os

from agents import Agent, Runner, function_tool
from dotenv import load_dotenv
from openinference.instrumentation.openai_agents import OpenAIAgentsInstrumentor

from gentrace import init, interaction

load_dotenv()

# Initialize Gentrace with OpenAI Agents instrumentation
init(
    api_key=os.getenv("GENTRACE_API_KEY"),
    base_url=os.getenv("GENTRACE_BASE_URL", "https://gentrace.ai/api"),
    otel_setup={
        "service_name": "openai-agents-demo",
        "instrumentations": [OpenAIAgentsInstrumentor()],
    },
)


@function_tool
def check_weather(city: str) -> str:
    """Get current weather for a city (simulated)."""
    # Simulated weather data
    weather_data = {
        "san francisco": "☁️ 62°F, cloudy",
        "new york": "☀️ 75°F, sunny",
        "london": "🌧️ 55°F, rainy",
    }
    return weather_data.get(city.lower(), f"No weather data for {city}")


@function_tool
def book_flight(from_city: str, to_city: str, date: str) -> str:
    """Book a flight (simulated)."""
    return (
        f"✈️ Flight booked from {from_city} to {to_city} on {date}. Confirmation: FL-{hash(from_city + to_city) % 10000}"
    )


# Create travel agent with tools
travel_agent = Agent(
    name="Travel Assistant",
    instructions="You are a helpful travel agent. You can check weather and book flights for customers.",
    tools=[check_weather, book_flight],
)


@interaction(name="travel_planning", pipeline_id=os.getenv("GENTRACE_PIPELINE_ID", ""))
def plan_trip(request: str) -> str:
    """Handle a travel planning request - automatically traced."""
    result = Runner.run_sync(
        starting_agent=travel_agent,
        input=request,
    )
    return str(result.final_output)


def main() -> None:
    """Run example with automatic tracing."""
    print("=== OpenAI Agents + OpenInference Example ===\n")

    # Single request that uses multiple tools
    response = plan_trip(
        "I want to fly from San Francisco to New York next Monday. What's the weather like in both cities?"
    )
    print(f"Response: {response}")

    print("\n✓ Agent conversation and tool calls have been traced!")
    print("Check your Gentrace dashboard to see the full trace.")


if __name__ == "__main__":
    main()
