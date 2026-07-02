import google.generativeai as genai
from fastapi import HTTPException

from dotenv import load_dotenv
import os

load_dotenv()


# Load from environment variable (safe for deployment)
GCP_API_KEY = os.getenv("GCP_API_KEY")

if not GCP_API_KEY:
    raise ValueError("GCP_API_KEY is not set in environment variables")

model = genai.GenerativeModel("gemini-2.5-flash")
    

def generate_message(conversations):
    try:
        print(conversations)

        history = []

        for convo in conversations[:-1]:
            history.append({
                "role": "user" if convo.role == "user" else "model",
                "parts": [convo.content]
            })

        print("History:", history)

        chat = model.start_chat(history=history)

        response = chat.send_message(conversations[-1].content)

        return response.text

    except Exception as e:
        print("ERROR:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
