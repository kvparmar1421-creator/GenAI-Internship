import os,json
from mistralai.client import Mistral
from dotenv import load_dotenv
load_dotenv()
client=Mistral(api_key=os.getenv("MISTRAL_API_KEY"))
menu={
"piza":199,
"burger":299,
"fries":99,
"coke":49,
"pepsi":49,
"sandwich":149,
"icecream":99,
"cake":199,
"milkshake":149
}
def get_menu():
    res=[]
    for item in menu:
        res.append({"item":item,"price":menu[item]})
    return res
tools=[{
    "type":"function",
    "function":{
    "name":"get_menu",
    "description":"get menu of restaurant",
    "parameters":{
        "type":"object",
        "properties":{}
        }
}
}
]
user_input=input("what can do for you : ")
message=[{"role":"user",
         "content":user_input}]
m=client.chat.complete(
    model="mistral-small-latest",
    temperature=0.3,
    messages=message,
    tools=tools,
    tool_choice="auto"
)
response=m.choices[0].message
if response.tool_calls:
    message.append(response)
    for tc in response.tool_calls:
        if tc.function.name=="get_menu":
            result=get_menu()
            formated_result=json.dumps(result)
            message.append({"role":"tool",
                            "content":formated_result,
                            "tool_call_id":tc.id
                            })
        final=client.chat.complete(
            model="mistral-small-latest",
            temperature=0.3,
            messages=message

        )
        print(final.choices[0].message.content)
    else:
        print(response.content)