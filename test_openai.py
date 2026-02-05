import os
from dotenv import load_dotenv
from openai import OpenAI

# Load .env file
load_dotenv()

# Get API key from ENV
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("❌ OPENAI_API_KEY not found in .env")
    exit()

# Create OpenAI client
client = OpenAI(api_key=api_key)

print("🔍 Testing OpenAI connection...")

try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": "Say hello in one short line"}
        ],
        timeout=20
    )

    print("\n✅ SUCCESS — OpenAI Key Works!")
    print("🤖 AI Response:")
    print(response.choices[0].message.content)

except Exception as e:
    print("\n❌ FAILED — OpenAI Key Not Working")
    print("Error:")
    print(e)
