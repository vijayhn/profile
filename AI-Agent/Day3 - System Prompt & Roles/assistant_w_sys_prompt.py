from openai import OpenAI
from dotenv import load_dotenv
import os

# Load configuration
load_dotenv()

# Create AI client
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

print("=" * 40)
print("      My AI Assistant")
print("=" * 40)

msgs=[{"role":"system",
       "content":"You are a helpful tour assistant.\
        You will provide information about tourist attractions,\
       and the iternary of the trip.\
        Keep it short and concise."}] 

while True:

    user_input = input("\nYou : ")

    msgs.append(
        {
        "role":"user",
        "content": user_input
        }
    )

    if user_input.lower() in ("quit","exit","bye"):
        print("\nAI  : Goodbye! Have a great day.")
        break

    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=msgs
    )

    ai_reply=response.choices[0].message.content
    print("\nAI :", ai_reply)

    msgs.append(
        {
        "role":"assistant",
        "content": ai_reply
        }
    )

    # print("\n------Conversation History------")
    # for msg in msgs:
    #     print(f"{msg['role'].title()} : {msg['content']}\n")