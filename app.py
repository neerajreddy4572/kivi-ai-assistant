import os
import requests
from fastapi import FastAPI, Request
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

app = FastAPI()

# ===== TOKENS FROM ENV =====
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ===== TELEGRAM API URL =====
TELEGRAM_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

# ===== OPENAI CLIENT =====
client = OpenAI(api_key=OPENAI_API_KEY)


# ===== REAL AI BRAIN FUNCTION =====
def ai_reply(user_text):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are Kivi, a smart, helpful personal AI assistant. Be clear and helpful."
                },
                {
                    "role": "user",
                    "content": user_text
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        print("AI Error:", str(e))
        return "⚠ AI is temporarily unavailable"


# ===== TELEGRAM WEBHOOK ENDPOINT =====
@app.post("/webhook")
async def telegram_webhook(request: Request):
    try:
        data = await request.json()
        print("Incoming Telegram Update:", data)

        if "message" in data:
            chat_id = data["message"]["chat"]["id"]
            text = data["message"].get("text", "")

            print("Chat ID:", chat_id)
            print("User Text:", text)

            reply = ai_reply(text)

            response = requests.post(
                TELEGRAM_URL,
                json={
                    "chat_id": chat_id,
                    "text": reply
                }
            )

            print("Telegram API Response:", response.text)

        return {"status": "ok"}

    except Exception as e:
        print("Webhook Error:", str(e))
        return {"status": "error"}


# ===== HEALTH CHECK =====
@app.get("/")
def home():
    return {"message": "Kivi AI Assistant is running 🚀"}
