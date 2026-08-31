import os
import json
import requests
from dotenv import load_dotenv

load_dotenv("../.env")

NVIDIA_API_KEY = os.environ.get("NVIDIA_API_KEY")

API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
MODEL = "nvidia/nemotron-3.5-lightning-30b-a3b"

STEP1_PROMPT = """
You are a news article claim extraction assistant.

Extract the core factual claims from the given news article.

Rules:
1. Extract only claims supported by the article.
2. Do not add outside information.
3. Do not add opinions or assumptions.
4. Keep each claim short and clear.
5. Return ONLY a valid JSON list of claims.
"""

STEP2_PROMPT = """
You are a news fact card generator.
Create a short fact card using ONLY the extracted claims provided.

The output must contain exactly:
Headline:
<short headline>
Key Facts:
- <fact 1>
- <fact 2>
- <fact 3>

Source Confidence:
<short confidence note>

Rules:
1. Use ONLY the extracted claims.
2. Do not use the original article.
3. Do not add outside information.
4. Do not invent facts.
5. Use exactly 3 bullet points.
6. Keep the fact card concise.
"""

article_text = input("Enter article text: ")

response = requests.post(
    API_URL,
    headers={
        "Authorization": f"Bearer {NVIDIA_API_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": STEP1_PROMPT
            },
            {
                "role": "user",
                "content": article_text
            }
        ],
        "temperature": 0
    }
)

claims_text = response.json()["choices"][0]["message"]["content"].strip()

claims = json.loads(claims_text)

print("\nStep 1 - Extracted Claims:")
for claim in claims:
    print("-", claim)


step2_input = f"""
Extracted Claims:

{json.dumps(claims, indent=2)}
"""

response = requests.post(
    API_URL,
    headers={
        "Authorization": f"Bearer {NVIDIA_API_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": STEP2_PROMPT
            },
            {
                "role": "user",
                "content": step2_input
            }
        ],
        "temperature": 0.3
    }
)

fact_card = response.json()["choices"][0]["message"]["content"].strip()

print("\nStep 2 - Fact Card:")
print(fact_card)