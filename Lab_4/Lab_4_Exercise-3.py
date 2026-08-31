import os
import requests
from dotenv import load_dotenv

load_dotenv("../.env")

NVIDIA_API_KEY = os.environ.get("NVIDIA_API_KEY")

API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
MODEL = "nvidia/nemotron-3.5-lightning-30b-a3b"

STEP1_PROMPT = """
You are a meeting discussion extraction assistant.

Extract the discussed points from the given meeting transcript.

Rules:
1. Extract only claims supported by the transcript.
2. Do not add outside information.
3. Keep each claim short and clear.
4. Return the discussion summary.
"""

STEP2_PROMPT = """
You are a meeting action item extraction assistant.

Identify action items from the extracted discussion points.

Rules:
1. Extract only action items supported by the discussion.
2. Do not add outside information.
3. Do not use the original transcript.
4. Identify the owner and deadline if mentioned.
5. If owner is missing, write "Missing".
6. If deadline is missing, write "Missing".
7. Flag missing owner or deadline.
8. Keep each action short and clear.
"""

STEP3_PROMPT = """
You are a meeting task formatting assistant.

Format the extracted discussion points and action items into a structured summary.

Rules:
1. Use ONLY the extracted discussion points and action items.
2. Do not use the original transcript.
3. Do not add outside information.
4. Keep the summary short and clean.
5. Format the final output as a Markdown table:

| Task | Owner | Deadline | Flag |
"""

transcript_text = input("Enter transcript text: ")

response = requests.post(
    API_URL,
    headers={
        "Authorization": f"Bearer {NVIDIA_API_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "model": MODEL,
        "messages": [
            {"role": "system", "content": STEP1_PROMPT},
            {"role": "user", "content": transcript_text}
        ],
        "temperature": 0
    }
)

step1_output = response.json()["choices"][0]["message"]["content"].strip()

print("\nSTEP 1 - DISCUSSION SUMMARY")
print(step1_output)


response = requests.post(
    API_URL,
    headers={
        "Authorization": f"Bearer {NVIDIA_API_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "model": MODEL,
        "messages": [
            {"role": "system", "content": STEP2_PROMPT},
            {"role": "user", "content": step1_output}
        ],
        "temperature": 0
    }
)

step2_output = response.json()["choices"][0]["message"]["content"].strip()

print("\nSTEP 2 - ACTION ITEMS")
print(step2_output)


step3_input = f"""
Discussion Summary:
{step1_output}

Action Items:
{step2_output}
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
            {"role": "system", "content": STEP3_PROMPT},
            {"role": "user", "content": step3_input}
        ],
        "temperature": 0
    }
)

step3_output = response.json()["choices"][0]["message"]["content"].strip()

print("\nSTEP 3 - FINAL TASK TABLE")
print(step3_output)