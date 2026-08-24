import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)

DOCTOR_SUMMARY_SYSTEM_PROMPT = """
You are a Doctor Consultation Summary Generator.

Your task is to analyze raw patient consultation notes and create a clean,
structured medical summary.

The input contains:
- Patient name
- Patient consultation notes

You must generate the following sections:

PATIENT NAME
SYMPTOMS
DIAGNOSIS
RECOMMENDATIONS
SUMMARY

Always use exactly this format:

PATIENT NAME:
<patient name>

SYMPTOMS:
- <symptom 1>
- <symptom 2>

DIAGNOSIS:
- <diagnosis>

RECOMMENDATIONS:
- <recommendation 1>
- <recommendation 2>

SUMMARY:
<short professional summary>

Rules:
1. Use the patient name exactly as provided.
2. Extract symptoms from the consultation notes.
3. Identify the diagnosis or clinical impression when it is documented
   in the notes.
4. Extract recommendations, treatment instructions, medications,
   tests, or follow-up instructions mentioned in the notes.
5. Do not invent information that is not supported by the notes.
6. Do not create a diagnosis solely from symptoms.
7. If diagnosis is not documented, write:
   - Not documented
8. If recommendations are not documented, write:
   - Not documented
9. Do not provide additional medical advice.
10. Keep the output concise and professional.
11. Always use the exact same section names and order.
12. Output only the final summary.
13. Do not output reasoning, analysis, <think> tags, or additional comments.
"""

print("Doctor Summary Generator")

patient_name = input("Enter patient name: ")
patient_notes = input("Enter patient notes: ")

prompt = f"""
Patient Name:
{patient_name}

Patient Consultation Notes:
{patient_notes}

Generate the doctor summary using the required format.
"""

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": DOCTOR_SUMMARY_SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": prompt
        }
    ],
    model="qwen/qwen3.6-27b"
)

output = chat_completion.choices[0].message.content

print("\nDoctor Summary:")
print(output)