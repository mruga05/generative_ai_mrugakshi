import os
import requests
from dotenv import load_dotenv

load_dotenv("../.env")

NVIDIA_API_KEY = os.environ.get("NVIDIA_API_KEY")

API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
MODEL = "nvidia/nemotron-3.5-lightning-30b-a3b"


def Ask_json(sys_prompt, content):
    response = requests.post(
        API_URL,
        headers={
            "Authorization": f"Bearer {NVIDIA_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": MODEL,
            "messages": [
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": content}
            ],
            "temperature": 0
        },
        timeout=60
    )

    return response.json()["choices"][0]["message"]["content"].strip()


STEP1_PROMPT = """
You are a product idea structuring assistant.

Expand the given one-line product idea into a structured pitch.

Structre should be:
1. Problem
2. Solution
3. Target User

Rules:
1. Use only information from the product idea.
2. Do not add information outside product idea.
3. Keep each section clear and short.
4. If information is not available, make a reasonable general interpretation.
5. Return only the structured pitch.
"""


STEP2_PROMPT = """
You are an investor pitch assistant.

Generate a short investor-style pitch paragraph using ONLY the
structured pitch provided by Step 1.

Rules:
1. Do not use the original product idea.
2. Do not add information that is not present in the structured pitch.
3. Clearly communicate the problem, solution, and target user.
4. Make it professional, and investor-friendly.
5. Return only the pitch paragraph.
"""


product_idea = input("Enter product idea: ")

step1_output = Ask_json(STEP1_PROMPT, product_idea)

print("\nSTEP 1 - STRUCTURED PITCH")
print(step1_output)


step2_output = Ask_json(STEP2_PROMPT, step1_output)

print("\nSTEP 2 - INVESTOR PITCH")
print(step2_output)