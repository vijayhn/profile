from openai import OpenAI
from dotenv import load_dotenv
from tools import get_current_time,roll_dice, generate_password
import os

load_dotenv()

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

from planner import choose_tool 

print("=" * 40)
print("      My AI Assistant")
print("=" * 40)

while True:

    user_input = input("\nYou : ")

    if user_input.lower() == "quit":
        print("\nAI  : Goodbye! Have a great day.")
        break

    tool= choose_tool(user_input)

    if tool == "get_current_time":

        result = get_current_time()

    elif tool == "roll_dice":

        result = roll_dice()

    elif tool == "generate_password":

        result = generate_password()

    else:

        result = None

    prompt= f"""
    The user asked: {user_input}

    The tool returned answer : {result}
    
    Please note that the date and time return from tool result is always date, month, year and time , not month first
    Answer the result in natural language keeping it crisp and concise. If the result is None, then asnwer from the LLM model knowledge. 
    """

    response = client.chat.completions.create(
    
    model=os.getenv("MODEL"),
    messages=[
            {
            "role":"user",
            "content":prompt
        }
        ]
    )
    print("\nAI :", response.choices[0].message.content)