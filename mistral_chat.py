import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Initialize the client
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.getenv("HUGGINGFACE_API_KEY")
)

def chat(user_message):
    """Send a message and get response"""
    completion = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3-8B-Instruct:novita",
        messages=[
            {"role": "user", "content": user_message}
        ]
    )
    
    return completion.choices[0].message.content

if __name__ == "__main__":
    user_input = input("You: ")
    print("AI:", chat(user_input))
