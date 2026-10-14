# quickstart.py
import os
from mistralai.client import Mistral
from dotenv import load_dotenv

load_dotenv()

client = Mistral(api_key="mstrl_FogicadWA467fGQB4d4gE7dDsbyzhfAH_4cUBiP")

response = client.chat.complete(
    model="mistral-small-latest",
    messages=[
        {"role": "system",
         
          "content": "your training institute name is abc training,which provide bca,bba,mba,msc,bcom.your institute time is 10am to 5pm."
          
          },
        {
            "role": "system",
            "content": "which course you provide ?"
        }
    ],
)

print(response.choices[0].message.content)