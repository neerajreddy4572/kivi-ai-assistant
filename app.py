import os
import requests
from fastapi import FastAPI, Request
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# Get token safely from .env / Render ENV
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Telegram send message URL
TELEGRAM_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"


# ===== AI BRAIN FUNCTION (TEMP VERSION) =====
def ai_reply(user_text):
    return f"🧠 Kivi AI: I understood → {user_text}"


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
