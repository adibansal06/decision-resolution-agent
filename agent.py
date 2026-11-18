
import os
import json

from dotenv import load_dotenv
from openai import OpenAI

from tool_schemas import TOOLS
from dispatcher import dispatch_tool


# ---------------- CONFIGURATION ----------------

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file.")

client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

MODEL = "openai/gpt-oss-20b"
MAX_ITERATIONS = 5


# ---------------- AGENT INSTRUCTIONS ----------------

SYSTEM_PROMPT = """
You are a customer support resolution agent for damaged-item orders.

Your job is to investigate an order and resolve the customer's complaint.

Follow this workflow carefully:

1. Always begin by calling lookup_order with the provided order ID.
2. If the order does not exist, explain that it could not be found.
   Do not process a refund or exchange.
3. If the order is already resolved (REFUNDED or EXCHANGED),
   explain its existing status. Do not repeat the transaction.
4. Check the order's exchange eligibility.
5. If the order is eligible, call check_inventory using the item's ID.
6. If the order is eligible AND stock is available:
   - Call process_exchange.
7. If the order is not eligible OR stock is unavailable:
   - Call process_refund with a clear reason.
8. After a successful refund or exchange:
   - Call notify_customer.
   - Use the registered customer email returned by lookup_order.
   - Write a clear and professional confirmation message.
9. Never claim that a refund, exchange, or notification succeeded
   unless the corresponding tool confirms success.
10. If a tool fails, explain the problem honestly.
11. If notification status is SIMULATED, explicitly say
    "Notification recorded (simulation); no actual email was sent."
12. Never describe a simulated notification as an email sent.
11. Never invent customer details, stock levels, or transaction results.

Return a concise final summary containing:
- Order ID
- Customer name, if available
- Resolution
- Reason
- Notification status

You may use the available tools to complete the workflow.
"""


# ---------------- REACT AGENT LOOP ----------------

def run_agent(user_query: str) -> str:

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_query}
    ]

    try:
        for iteration in range(MAX_ITERATIONS):

            print(f"\n[Agent iteration {iteration + 1}]")

            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=TOOLS,
                tool_choice="auto",
                temperature=0.2
            )

            assistant_message = response.choices[0].message

            # Case 1: The model wants to call one or more tools
            if assistant_message.tool_calls:

                # Preserve the assistant's tool-call message
                messages.append(
                    assistant_message.model_dump(exclude_none=True)
                )

                for tool_call in assistant_message.tool_calls:

                    tool_name = tool_call.function.name
                    arguments = tool_call.function.arguments

                    print(f"[Tool call] {tool_name}")
                    print(f"[Arguments] {arguments}")

                    # Execute only through our whitelist dispatcher
                    result = dispatch_tool(tool_name, arguments)

                    print(f"[Tool result] {result}")

                    # Return observation to the model
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(result)
                    })

                continue

            # Case 2: The model has produced its final answer
            if assistant_message.content:
                return assistant_message.content

            return "The agent could not generate a final response."

        # Iteration limit reached
        return (
            "The agent reached its maximum iteration limit. "
            "The request may require human review. "
            "Please verify the order status before taking further action."
        )

    except Exception as error:
        print(f"[Agent error] {error}")
        return (
            "An unexpected error occurred while processing the request. "
            "Please try again or contact support."
        )


# ---------------- RUN DIRECTLY ----------------

if __name__ == "__main__":

    print("\n===== CUSTOMER RESOLUTION AGENT =====")

    order_id = input("Enter the order ID: ").strip()

    if not order_id:
        print("Please provide a valid order ID.")
    else:
        query = (
            f"A customer has reported that their item arrived damaged. "
            f"Investigate and resolve order {order_id} "
            f"according to the resolution policy."
        )

        result = run_agent(query)

        print("\n========== FINAL RESOLUTION ==========")
        print(result)
