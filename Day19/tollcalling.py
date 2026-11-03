
from ddgs import DDGS
import os
import json
from mistralai.client import Mistral
from dotenv import load_dotenv

load_dotenv()

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

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


# Get menu
def get_menu():
    return json.dumps(menu)


# Web search
def web_search(query):
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=5))

    if results:
        return "\n".join(
            result["body"]
            for result in results
            if result.get("body")
        )

    return f"{query} not found"


# Check item price
def price_check(item):
    item = item.lower().strip()

    if item in menu:
        return f"{item}: ₹{menu[item]}"

    return "Item not found"


# Tool definitions
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_menu",
            "description": "Get the restaurant menu with item prices",
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
            "description": "Search the web for information",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query"
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
            "description": "Check the price of a menu item",
            "parameters": {
                "type": "object",
                "properties": {
                    "item": {
                        "type": "string",
                        "description": "The menu item name"
                    }
                },
                "required": ["item"]
            }
        }
    }
]


# Execute tools
def tool_call(name, args):

    if name == "get_menu":
        return get_menu()

    elif name == "web_search":
        return web_search(args["query"])

    elif name == "price_check":
        return price_check(args["item"])

    return "Tool not found"


# User input
user_input = input("Enter your query: ")

messages = [
    {
        "role": "user",
        "content": user_input
    }
]


# First Mistral API call
msg = client.chat.complete(
    model="mistral-small-latest",
    temperature=0.2,
    messages=messages,
    tools=tools,
    tool_choice="auto"
)


# Check API response
if not msg or not msg.choices:
    print("No response received from Mistral API.")
    exit()

response = msg.choices[0].message

if response is None:
    print("Mistral returned an empty message.")
    exit()


# Handle tool calls
if response.tool_calls:

    messages.append(response)

    for tc in response.tool_calls:

        print(f"\nTool used: {tc.function.name}")
        print(f"Arguments: {tc.function.arguments}")

        args = json.loads(tc.function.arguments)

        result = tool_call(
            tc.function.name,
            args
        )

        print(f"Tool output: {result}")

        messages.append({
            "role": "tool",
            "name": tc.function.name,
            "content": str(result),
            "tool_call_id": tc.id
        })


    # Final Mistral API call
    final = client.chat.complete(
        model="mistral-small-latest",
        temperature=0.2,
        messages=messages
    )

    if final and final.choices:
        print("\nFinal Answer:")
        print(final.choices[0].message.content)

    else:
        print("No final response received.")

else:

    if response.content:
        print("\nFinal Answer:")
        print(response.content)

    else:
        print("Mistral returned an empty response.")
