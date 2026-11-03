
from ddgs import DDGS
import os
import json
from mistralai.client import Mistral
from dotenv import load_dotenv

load_dotenv()

client = Mistral(
    api_key=os.getenv("MISTRAL_API_KEY")
)

# Restaurant Menu
menu = {
    "pizza": 199,
    "burger": 99,
    "fries": 49,
    "coke": 29,
    "pepsi": 29,
    "water": 19,
    "coffee": 49,
    "tea": 29,
    "icecream": 99,
    "cake": 199
}


# Tool 1: Get Menu
def get_menu():
    return json.dumps(menu)


# Tool 2: Web Search
def web_search(query):
    with DDGS() as ddgs:
        results = list(
            ddgs.text(query, max_results=5)
        )

    if results:
        return "\n".join(
            result["body"]
            for result in results
            if result.get("body")
        )

    return "No search results found."


# Tool 3: Price Check
def price_check(item):
    item = item.lower().strip()

    if item in menu:
        return f"{item}: ₹{menu[item]}"

    return "Item not found in the menu."


# Tool Definitions
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_menu",
            "description": "Get all restaurant menu items and prices",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the internet for information",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "price_check",
            "description": "Check the price of a restaurant item",
            "parameters": {
                "type": "object",
                "properties": {
                    "item": {
                        "type": "string",
                        "description": "Name of the menu item"
                    }
                },
                "required": ["item"]
            }
        }
    }
]


# Execute Tool
def tool_call(name, args):

    if name == "get_menu":
        return get_menu()

    elif name == "web_search":
        return web_search(args["query"])

    elif name == "price_check":
        return price_check(args["item"])

    return "Tool not found."


# AI Agent
def ai_agent(user_input):

    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful restaurant AI agent. "
                "Use the available tools to answer questions "
                "about menu items, prices, and web information. "
                "Give clear and simple answers."
            )
        },
        {
            "role": "user",
            "content": user_input
        }
    ]

    # Agent Loop
    for step in range(5):

        response = client.chat.complete(
            model="mistral-small-latest",
            temperature=0.2,
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        if not response or not response.choices:
            return "No response received from Mistral."

        assistant_message = response.choices[0].message

        if assistant_message is None:
            return "Mistral returned an empty message."

        # If no tool is required
        if not assistant_message.tool_calls:
            return assistant_message.content or "No answer generated."

        # Add assistant tool-call message
        messages.append(assistant_message)

        # Execute requested tools
        for tc in assistant_message.tool_calls:

            tool_name = tc.function.name

            print(f"\nTool Used: {tool_name}")

            args = json.loads(tc.function.arguments)

            print(f"Arguments: {args}")

            result = tool_call(
                tool_name,
                args
            )

            print(f"Tool Output: {result}")

            # Send result back to AI
            messages.append({
                "role": "tool",
                "name": tool_name,
                "content": str(result),
                "tool_call_id": tc.id
            })

    return "Agent stopped: maximum tool calls reached."


# Main Program
if __name__ == "__main__":

    print("================================")
    print("       RESTAURANT AI AGENT")
    print("================================")

    while True:

        user_input = input("\nYou: ")

        if user_input.lower() in ["exit", "quit", "stop"]:
            print("AI Agent: Goodbye!")
            break

        try:
            answer = ai_agent(user_input)

            print("\nAI Agent:", answer)

        except Exception as e:
            print("\nError:", e)
