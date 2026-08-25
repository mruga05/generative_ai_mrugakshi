import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv("../.env")

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.environ.get("NVIDIA_API_KEY")
)

MODEL = "nvidia/nemotron-3.5-lightning-30b-a3b"

STEP1_PROMPT = """
You are a job requirement extraction assistant.
Extract the key requirements from the raw job posting and return ONLY valid JSON.
Use exactly this structure:

{
    "job_title": "",
    "required_skills": [],
    "preferred_skills": [],
    "experience": "",
    "education": "",
    "responsibilities": []
}

Rules:
1. Extract information only from the job posting.
2. Do not invent requirements.
3. Keep required and preferred skills separate.
4. If information is not available, use an empty string or empty list.
5. Return only JSON.
"""

job_posting = input("Enter raw job posting: ")

step1_response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {
            "role": "system",
            "content": STEP1_PROMPT
        },
        {
            "role": "user",
            "content": job_posting
        }
    ],
    temperature=0
)

requirements_text = step1_response.choices[0].message.content.strip()

requirements = json.loads(requirements_text)

print("\nStep 1 - Structured Requirements:")
print(json.dumps(requirements, indent=2))

STEP2_PROMPT = """
You are a professional candidate outreach assistant.

Generate a personalized outreach message using ONLY:
1. The structured job requirements.
2. The candidate information.
Do NOT use the original job posting.

Rules:
- Do not invent candidate skills or experience.
- Mention relevant matches between the candidate and job requirements.
- Keep the message professional, friendly, and concise.
- Return only the outreach message.
"""

candidate_name = input("\nEnter candidate name: ")
candidate_profile = input("Enter candidate profile: ")

step2_input = f"""
Structured Job Requirements:
{json.dumps(requirements, indent=2)}

Candidate Name:
{candidate_name}

Candidate Profile:
{candidate_profile}
"""

step2_response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {
            "role": "system",
            "content": STEP2_PROMPT
        },
        {
            "role": "user",
            "content": step2_input
        }
    ],
    temperature=0.7
)

outreach_message = step2_response.choices[0].message.content.strip()

print("\nStep 2 - Personalized Outreach Message:")
print(outreach_message)