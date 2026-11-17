
import os
import json

from mistralai.client import Mistral
from dotenv import load_dotenv

load_dotenv()

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))


# DATABASE

orders = {
    "ORD101": "Shipped - arriving tomorrow",
    "ORD102": "Packed - shipping tomorrow",
    "ORD103": "Out for delivery - agent nearby"
}

menu = {
    "bhajiya": 50,
    "puff": 30,
    "samosa": 40,
    "water": 20
}


# ORDER TRACKING TOOL

def track_order(order_id):

    order_id = order_id.upper()

    if order_id in orders:
        return orders[order_id]

    return "Order not found."


# MENU TOOL

def get_menu():

    result = ""

    for k, v in menu.items():
        result += k + " - Rs " + str(v) + "\n"

    return result


# PRICE CHECK TOOL

def checkprice(item):

    item = item.lower()

    if item in menu:
        return item + " costs Rs " + str(menu[item])

    return item + " is not in the menu."


# TOOL EXECUTION

def run_tool(name, args):

    if name == "track_order":
        return track_order(args["order_id"])

    elif name == "get_menu":
        return get_menu()

    elif name == "checkprice":
        return checkprice(args["item"])

    else:
        return "Unknown Tool"


# ORDER TOOL DEFINITION

order_tool = [
    {
        "type": "function",
        "function": {
            "name": "track_order",
            "description": "Track an order using its order ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "Example: ORD101"
                    }
                },
                "required": ["order_id"]
            }
        }
    }
]


# MENU TOOL DEFINITION

menu_tool = [
    {
        "type": "function",
        "function": {
            "name": "get_menu",
            "description": "Get the complete food menu with prices.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "checkprice",
            "description": "Get the price of a particular dish.",
            "parameters": {
                "type": "object",
                "properties": {
                    "item": {
                        "type": "string",
                        "description": "Dish name"
                    }
                },
                "required": ["item"]
            }
        }
    }
]


# MAIN AGENT

def run_main(system_prompt, query, tools):

    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": query
        }
    ]

    response = client.chat.complete(
        model="mistral-small-latest",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    msg = response.choices[0].message

    if msg.tool_calls:

        messages.append(msg)

        for tc in msg.tool_calls:

            args = json.loads(tc.function.arguments)

            result = run_tool(
                tc.function.name,
                args
            )

            print(f"{tc.function.name} => {result}")

            messages.append({
                "role": "tool",
                "name": tc.function.name,
                "content": str(result),
                "tool_call_id": tc.id
            })

        final = client.chat.complete(
            model="mistral-small-latest",
            messages=messages
        )

        return final.choices[0].message.content

    return msg.content


# ROUTER AGENT

def router(query):

    router_client = client.chat.complete(
        model="mistral-small-latest",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": """
                You are a query router.

                Reply with ONE word only:

                order - Order tracking and delivery questions.
                menu - Food menu and price questions.
                general - Everything else.
                """
            },
            {
                "role": "user",
                "content": query
            }
        ]
    )

    return router_client.choices[0].message.content.strip().lower()


# MAIN APPLICATION

query = input("BOT: ")

category = router(query)

print(f"Routed to: {category} Agent")


if category == "order":

    answer = run_main(
        "You are a polite order support agent. Use the track_order tool to help customers.",
        query,
        order_tool
    )

elif category == "menu":

    answer = run_main(
        "You are a friendly menu assistant. Use get_menu and checkprice tools to help customers.",
        query,
        menu_tool
    )

else:

    answer = run_main(
        "You are a helpful support agent. Answer customers politely.",
        query,
        []
    )


# FINAL RESPONSE

print("\nSupport:", answer)