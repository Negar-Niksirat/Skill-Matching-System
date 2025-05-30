import os
import requests
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv("API_KEY")

def chat_with_chatbot(user_prompt: str) -> str:

    prompt = (user_prompt)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant who answer to questions."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].strip()
    else:
        raise Exception(f"❌ API Error {response.status_code}: {response.text}")