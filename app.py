import os
import time
import requests
from fastapi import FastAPI, Request
from dotenv import load_dotenv
from openai import OpenAI

# ===== LOAD ENV =====
load_dotenv()

app = FastAPI()

# ===== TOKENS FROM ENV =====
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not TELEGRAM_TOKEN:
    raise Exception("TELEGRAM_TOKEN missing in ENV")

if not OPENAI_API_KEY:
    raise Exception("OPENAI_API_KEY missing in ENV")

# ===== TELEGRAM API URL =====
TELEGRAM_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

# ===== OPENAI CLIENT =====
client = OpenAI(api_key=OPENAI_API_KEY)

# ===== REAL AI BRAIN FUNCTION =====
def ai_reply(user_text):
    """
    Stable AI reply with retry logic.
    """

    for attempt in range(2):   # Retry once if fail
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": """
You are Kivi AI.
You help with:
- Daily planning
- Prompt engineering help
- Task management
- Smart suggestions
- Decision support
- Friendly AI chat

Be clear, helpful, and practical.
"""
                    },
                    {
                        "role": "user",
                        "content": user_text
                    }
                ],
                timeout=20
            )

            return response.choices[0].message.content

        except Exception as e:
            print(f"AI Attempt {attempt+1} Failed:", str(e))
            time.sleep(2)

    return "⚠ AI is temporarily unavailable. Try again in a few seconds."


# ===== TELEGRAM SEND FUNCTION =====
def send_telegram(chat_id, text):
    try:
        response = requests.post(
            TELEGRAM_URL,
            json={
                "chat_id": chat_id,
                "text": text
            },
            timeout=15
        )

        print("Telegram Response:", response.text)

    except Exception as e:
        print("Telegram Send Error:", str(e))


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

            if text:
                reply = ai_reply(text)
                send_telegram(chat_id, reply)

        return {"status": "ok"}

    except Exception as e:
        print("Webhook Error:", str(e))
        return {"status": "error"}


# ===== HEALTH CHECK =====
@app.get("/")
def home():
    return {"message": "Kivi AI Assistant is running 🚀"}
