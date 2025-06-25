"""
OpenAI Agents instrumentation example using OpenInference with Gentrace.

This example demonstrates how to use OpenInference instrumentation with the OpenAI Agents
Python SDK (formerly known as Swarm). It shows:

1. Setting up OpenInference instrumentation for OpenAI Agents
2. Creating agents with specific capabilities and tools
3. Enabling agent handoffs for complex workflows
4. Automatic tracing of agent interactions, tool calls, and handoffs

The OpenInference instrumentation captures:
- Full agent conversations and responses
- Tool invocations and their results
- Agent handoffs and context transfers
- Model parameters and metadata

This provides comprehensive observability for agent-based applications.
"""

import os

from agents import Agent, Runner, function_tool
from openinference.instrumentation.openai_agents import OpenAIAgentsInstrumentor

import gentrace
from gentrace import interaction

# Pipeline ID for tracking
PIPELINE_ID = os.getenv("GENTRACE_PIPELINE_ID", "26d64c23-e38c-56fd-9b45-9adc87de797b")

# Initialize Gentrace with OpenAI Agents instrumentation
gentrace.init(
    api_key=os.getenv("GENTRACE_API_KEY"),
    base_url=os.getenv("GENTRACE_BASE_URL", "https://gentrace.ai/api"),
    otel_setup={
        "service_name": "openai-agents-instrumentation-demo",
        "instrumentations": [OpenAIAgentsInstrumentor()],
    },
)


# Define tools that agents can use
@function_tool
def calculate_discount(original_price: float, discount_percentage: float) -> str:
    """Calculate the discounted price for a product."""
    discount_amount = original_price * (discount_percentage / 100)
    final_price = original_price - discount_amount
    return (
        f"Original price: ${original_price:.2f}\n"
        f"Discount: {discount_percentage}%\n"
        f"Discount amount: ${discount_amount:.2f}\n"
        f"Final price: ${final_price:.2f}"
    )


@function_tool
def check_inventory(product_name: str) -> str:
    """Check inventory levels for a product (simulated)."""
    # Simulated inventory data
    inventory = {
        "laptop": {"in_stock": 15, "warehouse": "A"},
        "phone": {"in_stock": 32, "warehouse": "B"},
        "tablet": {"in_stock": 0, "warehouse": "C"},
        "headphones": {"in_stock": 45, "warehouse": "A"},
    }
    
    product_lower = product_name.lower()
    if product_lower in inventory:
        stock_info = inventory[product_lower]
        in_stock = stock_info["in_stock"]
        if isinstance(in_stock, int) and in_stock > 0:
            return (
                f"Product: {product_name}\n"
                f"Available: Yes\n"
                f"Quantity: {in_stock}\n"
                f"Warehouse: {stock_info['warehouse']}"
            )
        else:
            return f"Product: {product_name}\nAvailable: No\nQuantity: 0"
    return f"Product '{product_name}' not found in inventory"


# Create specialized agents
sales_agent = Agent(
    name="Sales Assistant",
    instructions="""You are a helpful sales assistant. You can:
    - Help customers find products
    - Calculate discounts and pricing
    - Check product availability
    When a customer needs technical support, transfer them to the Technical Support agent.""",
    tools=[calculate_discount, check_inventory],
)

tech_support_agent = Agent(
    name="Technical Support",
    instructions="""You are a technical support specialist. You help customers with:
    - Product setup and configuration
    - Troubleshooting technical issues
    - Providing technical specifications
    For sales-related questions, transfer back to the Sales Assistant.""",
)


# Define handoff functions
def transfer_to_tech_support() -> Agent:
    """Transfer the conversation to technical support."""
    return tech_support_agent


def transfer_to_sales() -> Agent:
    """Transfer the conversation back to sales."""
    return sales_agent


# Add handoff capabilities using handoffs parameter
sales_agent = Agent(
    name="Sales Assistant",
    instructions="""You are a helpful sales assistant. You can:
    - Help customers find products
    - Calculate discounts and pricing
    - Check product availability
    When a customer needs technical support, transfer them to the Technical Support agent.""",
    tools=[calculate_discount, check_inventory],
    handoffs=[tech_support_agent],
)

tech_support_agent = Agent(
    name="Technical Support",
    instructions="""You are a technical support specialist. You help customers with:
    - Product setup and configuration
    - Troubleshooting technical issues
    - Providing technical specifications
    For sales-related questions, transfer back to the Sales Assistant.""",
    handoffs=[sales_agent],
)


@interaction(name="customer_service_flow", pipeline_id=PIPELINE_ID)
def handle_customer_query(query: str) -> str:
    """Handle a customer service query with multiple agents."""
    # Start with the sales agent
    result = Runner.run_sync(
        starting_agent=sales_agent,
        input=query,
        max_turns=10,  # Allow multiple agent interactions
    )
    
    return str(result.final_output)


@interaction(name="multi_turn_conversation", pipeline_id=PIPELINE_ID)
def multi_turn_example() -> str:
    """Demonstrate a multi-turn conversation with agent handoffs."""
    # First query - sales related
    result1 = Runner.run_sync(
        starting_agent=sales_agent,
        input="Hi, I'm interested in buying a laptop. What's the price with a 15% discount if it costs $1200?"
    )
    print(f"Sales Agent: {result1.final_output}\n")
    
    # Second query - technical question (should trigger handoff)
    # Convert the result to input list and add the new user message
    input2 = result1.to_input_list() + [{"role": "user", "content": "Great! But I'm having trouble with my current laptop. It won't connect to WiFi. Can you help?"}]
    result2 = Runner.run_sync(
        starting_agent=sales_agent,
        input=input2
    )
    print(f"Tech Support: {result2.final_output}\n")
    
    # Third query - back to sales (should trigger handoff back)
    input3 = result2.to_input_list() + [{"role": "user", "content": "Thanks for the help! Now, can you check if the new laptop is in stock?"}]
    result3 = Runner.run_sync(
        starting_agent=sales_agent,
        input=input3
    )
    print(f"Sales Agent: {result3.final_output}\n")
    
    return str(result3.final_output)


def main() -> None:
    """Run example demonstrations."""
    print("=== OpenAI Agents Instrumentation Example ===\n")
    
    # Example 1: Simple single query
    print("Example 1: Single Query with Tool Use")
    print("-" * 40)
    response = handle_customer_query(
        "I want to buy headphones. Can you check if they're in stock and calculate the price with a 20% discount on $150?"
    )
    print(f"Response: {response}\n")
    
    # Example 2: Multi-turn conversation with handoffs
    print("\nExample 2: Multi-turn Conversation with Agent Handoffs")
    print("-" * 40)
    multi_turn_example()
    
    print("\n✓ All agent interactions, tool calls, and handoffs have been traced!")
    print("View the traces in your Gentrace dashboard to see:")
    print("  - Complete agent conversations")
    print("  - Tool invocations and results")
    print("  - Agent handoffs and context transfers")
    print("  - Token usage and latency metrics")


if __name__ == "__main__":
    main()