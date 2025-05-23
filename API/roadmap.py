import os
import requests
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv("API_KEY")

def generate_learning_roadmap(missing_skills: list[str], role_title: str) -> str:
    if not missing_skills:
        return "✅ You already have all the key skills for this role!"

    skills_text = ", ".join(missing_skills)
    prompt = (
        f"Please provide a structured and practical roadmap to learn the following skills needed for a '{role_title[0]}' role: "
        f"{skills_text}. Focus on learning order, resources, and milestones in a beginner-friendly and motivating tone."
    )

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant who provides clear learning roadmaps."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].strip()
    else:
        raise Exception(f"❌ API Error {response.status_code}: {response.text}")