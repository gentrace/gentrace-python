"""Simple LangChain example with Gentrace instrumentation using OpenInference."""
# pyright: reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false
# mypy: ignore-errors

import os

from dotenv import load_dotenv

# LangChain imports
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from openinference.instrumentation.langchain import LangChainInstrumentor

from gentrace import init, interaction

load_dotenv()

# Initialize Gentrace with LangChain instrumentation
init(
    api_key=os.getenv("GENTRACE_API_KEY"),
    base_url=os.getenv("GENTRACE_BASE_URL", "https://api.gentrace.ai"),
    otel_setup={"service_name": "langchain-example", "instrumentations": [LangChainInstrumentor()]},
)


def main() -> None:
    """Run a simple LangChain example with pipeline tracking."""
    # Check if we have the required environment variables
    if not os.getenv("OPENAI_API_KEY"):
        print("Please set OPENAI_API_KEY environment variable")
        return

    if not os.getenv("GENTRACE_API_KEY"):
        print("Please set GENTRACE_API_KEY environment variable")
        return

    # Create components
    llm = ChatOpenAI(model="gpt-4.1", temperature=0)

    prompt = ChatPromptTemplate.from_messages(
        [("system", "You are a helpful assistant that explains technical concepts simply."), ("human", "{topic}")]
    )

    # Create chain
    chain = prompt | llm | StrOutputParser()

    # Create instrumented function
    @interaction(pipeline_id=os.getenv("GENTRACE_PIPELINE_ID", ""))
    def run_chain() -> str:
        result = chain.invoke({"topic": "What is OpenTelemetry?"})
        print(f"Response: {result}")
        return result

    # Run the chain with pipeline tracking
    run_chain()

    print("\nCheck your Gentrace dashboard for traces!")


if __name__ == "__main__":
    main()
