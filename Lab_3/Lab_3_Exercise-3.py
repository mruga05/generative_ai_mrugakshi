import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)

SYSTEM_PROMPT = """
You are a resume field extractor assistant.

Your task is to extract only the fields requested by the user from the
provided resume text and return them as valid JSON. Id requested fields are not there return null.

Rules:
1. Extract ONLY the requested fields.
2. Return ONLY valid JSON.
3. Do not provide explanations or suggestions.
4. Do not add fields that were not requested.
5. If a requested field is not available in the resume, return null.
6. Do not guess or invent information.
7. Use the exact field names requested by the user.

Example:
Resume: Mrugakshi Kulkarni
Email: mk05@gmail.com
Phone: 9876543210
Skills: Python, SQL, Power BI
Education: B.Tech Computer Science

Requested fields:
name, email, skills

Output:
{
  "name": "Mrugakshi Kulkarni",
  "email": "mk05@gmail.com",
  "skills": ["Python", "SQL", "Power BI"]
}
"""

resume_text = input("Enter resume text: ")
fields_to_extract = input("Enter fields to extract (comma separated): ")

prompt = f"""
Resume Text:
{resume_text}

Fields to Extract:
{fields_to_extract}

Return only a valid JSON object containing exactly the requested fields.
"""

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": prompt
        }
    ],
    model="qwen/qwen3.6-27b"
)

output = chat_completion.choices[0].message.content.strip()

print(output)