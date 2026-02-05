import os
import time
import requests
from fastapi import FastAPI, Request
from dotenv import load_dotenv

# ===== LOAD ENV =====
load_dotenv()

app = FastAPI()

# ===== ENV VARIABLES =====
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
HF_API_KEY = os.getenv("HF_API_KEY")

if not TELEGRAM_TOKEN:
    raise Exception("TELEGRAM_TOKEN missing in ENV")

if not HF_API_KEY:
    raise Exception("HF_API_KEY missing in ENV")

# ===== TELEGRAM API =====
TELEGRAM_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

# ===== HUGGINGFACE MODEL =====
HF_MODEL_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"

HF_HEADERS = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json"
}


# ===== FREE AI BRAIN FUNCTION =====
def ai_reply(user_text):
    """
    Free AI using HuggingFace Inference API
    """

    prompt = f"""
You are Kivi AI.
You act as:
- Day planner
- Prompt engineer
- Task planner
- Schedule maker
- Decision helper
- Friendly assistant

User: {user_text}
Assistant:
"""

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 250,
            "temperature": 0.7,
            "return_full_text": False
        }
    }

    for attempt in range(2):  # retry once
        try:
            response = requests.post(
                HF_MODEL_URL,
                headers=HF_HEADERS,
                json=payload,
                timeout=30
            )

            result = response.json()

            if isinstance(result, list) and "generated_text" in result[0]:
                return result[0]["generated_text"].strip()

            if "error" in result:
                print("HF Error:", result["error"])
                time.sleep(2)

        except Exception as e:
            print("HF Exception:", str(e))
            time.sleep(2)

    return "⚠ Free AI is busy right now. Please try again in a moment."


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


# ===== TELEGRAM WEBHOOK =====
@app.post("/webhook")
async def telegram_webhook(request: Request):
    try:
        data = await request.json()
        print("Incoming Update:", data)

        if "message" in data:
            chat_id = data["message"]["chat"]["id"]
            text = data["message"].get("text", "").strip()

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
