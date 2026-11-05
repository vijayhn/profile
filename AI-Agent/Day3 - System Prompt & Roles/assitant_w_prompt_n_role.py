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

roles = {
    "1": "You are a friendly school teacher. Explain every concept using simple language and real-life examples.",
    "2": "You are a senior Python developer. Explain programming concepts clearly and always include Python examples.",
    "3": "You are an experienced travel guide. Recommend places, food, transportation and travel tips.",
    "4": "You are a motivational coach. Encourage the user and give practical advice with a positive attitude.",
    "5": "You are a professional interviewer. Ask one interview question at a time and provide feedback after each answer.",
    "6": "You are a Professional personal trainer and dietician. You can give tips on exercising and food habits."
}

def display_menu():
    print("\nAvailable Assistants:")
    print("1. Teacher")
    print("2. Python Expert")
    print("3. Travel Guide")
    print("4. Motivational Coach")
    print("5. Interviewer")
    print("6. Personal Trainer")

# Initial setup
display_menu()
choice = input("\nEnter your choice : ")

messages = [
    {
        "role": "system",
        "content": roles.get(choice, "You are a helpful AI assistant.")
    }
]

print("\n(Tip: Type '/role' at any time to switch personas or 'quit' to exit)\n")

while True:
    user_input = input("\nYou : ")

    if user_input.lower() == "quit":
        print("\nAI  : Goodbye! Have a great day.")
        break

    # --- Role Switching Logic ---
    if user_input.lower() == "/role":
        display_menu()
        new_choice = input("\nEnter your new choice number: ")
        
        if new_choice in roles:
            # FIX: We modify ONLY the content of the very first element (index 0) in the list.
            messages[0]["content"] = roles[new_choice]
            print(f"\n[System: Persona changed to option {new_choice}! Previous chat memory preserved.]")
        else:
            print("\n[System: Invalid choice. Keeping current role.]")
        continue 
    # -----------------------------

    # Save the user's message
    messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=messages
    )

    # Note: Added [0] here because your original script used response.choices[0].message.content
    ai_reply = response.choices[0].message.content

    print("\nAI :", ai_reply)

    # Save the AI's reply
    messages.append(
        {
            "role": "assistant",
            "content": ai_reply
        }
    )
