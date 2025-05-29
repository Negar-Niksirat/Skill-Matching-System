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
        "Provide a clear and structured learning roadmap for the following skills missing from the user's resume, required for the role of "
        + str(role_title) + ": "
        + ", ".join(missing_skills)
        + ".\n"
        "For each skill:\n"
        "- Suggest one high-quality learning resource (course, book, tutorial, etc.)\n"
        "- Add a brief explanation (1-2 sentences) on what the resource covers and why it's effective.\n"
        "Do not include any extra commentary, introductions, or conclusions. Just output the roadmap."
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