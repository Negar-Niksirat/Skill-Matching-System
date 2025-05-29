import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")

def skills_process(all_skills_str: str, api_key: str) -> str:
    prompt = "Extract the main keywords from the following list of skills. Only return the keywords in a Python set format. Each keyword should be lowercase, in single quotes, and separated by commas. Do not include extra text, explanations, or symbols. Example output: {'python', 'sql', 'big data'}\n\n"+ all_skills_str
  
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that returns a list of skills exactly in Python set format."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].strip()
    else:
        raise Exception(f"❌ Error {response.status_code}: {response.text}")