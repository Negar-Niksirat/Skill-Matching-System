import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")

def summarize_job_descriptions(job_descriptions: list[str], role_title: str) -> str:
    if not job_descriptions:
        return "No job descriptions provided."

    combined_text = "\n\n".join(job_descriptions)
    prompt = (
        f"Please combine and summarize the following job descriptions about '{role_title}' "
        "into a single, clear, and engaging paragraph of maximum 2 sentences. "
        "Focus on the main responsibilities, goals, and impact of the role in simple, professional language.\n\n"
        f"{combined_text}"
    )

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that summarizes job descriptions."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].strip()
    else:
        raise Exception(f"❌ API Error {response.status_code}: {response.text}")
