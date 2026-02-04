import os
import requests
from fastapi import FastAPI, Request
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# Get token safely from .env
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Telegram send message URL
TELEGRAM_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"


# ===== AI BRAIN FUNCTION (TEMP VERSION) =====
def ai_reply(user_text):
    """
    Temporary AI reply.
    Later we will connect real AI API here.
    """
    return f"🧠 Kivi AI: I understood → {user_text}"


# ===== TELEGRAM WEBHOOK ENDPOINT =====
@app.post("/webhook")
async def telegram_webhook(request: Request):

    data = await request.json()

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        reply = ai_reply(text)

        requests.post(
            TELEGRAM_URL,
            json={
                "chat_id": chat_id,
                "text": reply
            }
        )

    return {"status": "ok"}


# ===== HEALTH CHECK =====
@app.get("/")
def home():
    return {"message": "Kivi AI Assistant is running 🚀"}
