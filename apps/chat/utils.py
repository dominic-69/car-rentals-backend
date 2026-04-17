import requests
from django.conf import settings

def get_ai_reply(message):
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "mistralai/mistral-7b-instruct",
                "messages": [
                    {"role": "system", "content": "You are a helpful car assistant."},
                    {"role": "user", "content": message}
                ]
            }
        )

        data = response.json()

        return data["choices"][0]["message"]["content"]

    except Exception as e:
        return None
    
import requests

def call_fastapi(message):
    try:
        response = requests.post(
            "http://127.0.0.1:8001/ai/chat/",
            json={"message": message}
        )
        return response.json().get("reply")
    except Exception as e:
        print("FastAPI Error:", e)
        return None