"""
This example demonstrates integrating Pydantic AI with Gentrace for enhanced observability.
Pydantic AI already uses OpenTelemetry, so Gentrace automatically captures traces while
adding essential attributes like pipeline_id for proper rendering in the Gentrace dashboard.

Prerequisites:
    GENTRACE_API_KEY: Your Gentrace API token
    OPENAI_API_KEY: Your OpenAI API key
    GENTRACE_BASE_URL: Your Gentrace instance URL (e.g., http://localhost:3000)
    GENTRACE_PIPELINE_ID: Your pipeline ID (must be a valid UUID)
"""

import os
import random
import asyncio
from typing import Any, Dict, List
from datetime import datetime
from dataclasses import dataclass

from pydantic import Field, BaseModel
from pydantic_ai import Agent, RunContext
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from pydantic_ai.models.openai import OpenAIModel
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

from gentrace import GentraceSampler, GentraceSpanProcessor, interaction

# Environment setup
api_key = os.getenv("GENTRACE_API_KEY", "")
openai_api_key = os.getenv("OPENAI_API_KEY", "")
gentrace_base_url = os.getenv("GENTRACE_BASE_URL", "")
pipeline_id = os.getenv("GENTRACE_PIPELINE_ID", "")

if not api_key:
    raise ValueError("GENTRACE_API_KEY environment variable not set.")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set.")
if not gentrace_base_url:
    raise ValueError("GENTRACE_BASE_URL environment variable not set.")
if not pipeline_id:
    raise ValueError("GENTRACE_PIPELINE_ID environment variable not set.")

# Configure OpenTelemetry with Gentrace
resource = Resource(attributes={"service.name": "pydantic-ai-gentrace-example"})
tracer_provider = TracerProvider(resource=resource, sampler=GentraceSampler())

# Configure OTLP exporter with Gentrace endpoint
otlp_headers: Dict[str, str] = {"Authorization": f"Bearer {api_key}"}
span_exporter = OTLPSpanExporter(
    endpoint=f"{gentrace_base_url}/otel/v1/traces",
    headers=otlp_headers,
)

# Add Gentrace span processor for baggage enrichment
gentrace_baggage_processor = GentraceSpanProcessor()
tracer_provider.add_span_processor(gentrace_baggage_processor)

# Add export processor
simple_export_processor = SimpleSpanProcessor(span_exporter)
tracer_provider.add_span_processor(simple_export_processor)
trace.set_tracer_provider(tracer_provider)

# Initialize Pydantic AI model
model = OpenAIModel("gpt-4o")


@dataclass
class UserContext:
    name: str
    preferences: str


# Models for book data
class BookDetails(BaseModel):
    title: str = Field(description="Book title")
    author: str = Field(description="Book author")
    genre: str = Field(description="Book genre")
    rating: float = Field(description="Average rating")
    available: bool = Field(description="Availability status")


# Enable PydanticAI instrumentation for all agents
Agent.instrument_all()

# Create a Pydantic AI agent
agent = Agent(
    model=model,
    deps_type=UserContext,
    system_prompt="You are a helpful assistant that provides personalized book recommendations. Use the available tools to find books and check their availability.",
)


# Mock book database
BOOKS_DB: List[BookDetails] = [
    BookDetails(title="Dune", author="Frank Herbert", genre="science fiction", rating=4.5, available=True),
    BookDetails(title="Foundation", author="Isaac Asimov", genre="science fiction", rating=4.3, available=True),
    BookDetails(title="1984", author="George Orwell", genre="dystopian", rating=4.2, available=False),
    BookDetails(title="The Martian", author="Andy Weir", genre="science fiction", rating=4.6, available=True),
    BookDetails(title="Neuromancer", author="William Gibson", genre="cyberpunk", rating=4.0, available=True),
]


# Tool without context - searches for books by genre
@agent.tool_plain
def search_books_by_genre(genre: str) -> List[Dict[str, str]]:
    """Search for books by genre.
    
    Args:
        genre: The genre to search for (e.g., 'science fiction', 'dystopian')
    """
    matching_books = [
        {
            "title": book.title,
            "author": book.author,
            "rating": str(book.rating)
        }
        for book in BOOKS_DB
        if genre.lower() in book.genre.lower()
    ]
    return matching_books


# Tool with context - gets detailed book information
@agent.tool
def get_book_details(ctx: RunContext[UserContext], title: str) -> Dict[str, Any]:
    """Get detailed information about a specific book.
    
    Args:
        title: The title of the book to look up
    """
    for book in BOOKS_DB:
        if book.title.lower() == title.lower():
            # Add personalized note based on user preferences
            personalized = "matches your preferences" if ctx.deps.preferences.lower() in book.genre.lower() else "different genre"
            return {
                "title": book.title,
                "author": book.author,
                "genre": book.genre,
                "rating": book.rating,
                "available": book.available,
                "personalized_note": f"This book {personalized}!"
            }
    return {"error": f"Book '{title}' not found"}


# Tool to check real-time availability
@agent.tool_plain
def check_availability(title: str) -> str:
    """Check if a book is currently available.
    
    Args:
        title: The title of the book to check
    """
    # Simulate checking availability with timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for book in BOOKS_DB:
        if book.title.lower() == title.lower():
            if book.available:
                # Simulate random stock levels
                stock = random.randint(1, 5)
                return f"'{book.title}' is available (Stock: {stock} copies) as of {current_time}"
            else:
                return f"'{book.title}' is currently out of stock as of {current_time}"
    return f"Book '{title}' not found in our system"


@interaction(pipeline_id=pipeline_id, name="pydantic_ai_recommendation")
async def get_recommendation(user: UserContext) -> str:
    """Get a personalized recommendation using Pydantic AI."""
    result = await agent.run(f"Give a brief recommendation for {user.name} who likes {user.preferences}.")  # type: ignore
    return result.output


@interaction(pipeline_id=pipeline_id, name="pydantic_ai_structured_output")
async def analyze_sentiment(text: str) -> Dict[str, str]:
    """Analyze sentiment with structured output."""
    sentiment_agent = Agent(
        model=model,
        system_prompt="Analyze the sentiment of the given text. Return only: positive, negative, or neutral.",
    )

    result = await sentiment_agent.run(f"Analyze sentiment: {text}")  # type: ignore

    return {"text": text, "sentiment": result.output, "model": "gpt-4o"}


@interaction(pipeline_id=pipeline_id, name="book_recommendation_with_tools")
async def get_book_recommendation_with_tools(user: UserContext) -> str:
    """Get book recommendations using tools."""
    result = await agent.run(  # type: ignore
        f"Find some {user.preferences} for {user.name}. Check their availability and recommend the best ones with highest ratings.",
        deps=user
    )
    return result.output


@interaction(pipeline_id=pipeline_id, name="direct_tool_test")
async def test_direct_tool(user: UserContext) -> str:
    """Test tools directly."""
    result = await agent.run(   # type: ignore
        "Check if 'Dune' is available right now",
        deps=user
    )
    return result.output


async def main() -> None:
    # Example 1: Get personalized recommendation with tools
    user = UserContext(name="Alice", preferences="science fiction books")
    
    recommendation = await get_book_recommendation_with_tools(user)
    print(f"Book recommendation for {user.name}:\n{recommendation}\n")

    # Example 2: Simple recommendation without tools
    simple_recommendation = await get_recommendation(user)
    print(f"Simple recommendation: {simple_recommendation}")

    # Example 3: Analyze sentiment
    sentiment_result = await analyze_sentiment("I love using Gentrace with Pydantic AI!")
    print(f"\nSentiment analysis: {sentiment_result}")

    # Example 4: Test specific tool directly
    availability = await test_direct_tool(UserContext(name="Test User", preferences="any"))
    print(f"\nAvailability check: {availability}")

    print("\n✨ Check your Gentrace dashboard to see the tool call traces!")


if __name__ == "__main__":
    asyncio.run(main())
    # Ensure spans are exported before exit
    tracer_provider.shutdown()
