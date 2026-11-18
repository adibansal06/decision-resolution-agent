
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load the API key from .env
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("Groq API key not found!")

# Connect to Groq using the OpenAI SDK
client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)

# Send a test request
response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role": "user",
            "content": "Explain an AI agent in two simple sentences."
        }
    ]
)

print("\nAI RESPONSE:")
print(response.choices[0].message.content)
