import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)

SYSTEM_PROMPT = """
You are a professional customer support assistant.

Your task is to write a helpful and polite reply to a customer message.

Rules:
1. Always use a professional, friendly, and empathetic tone.
2. Mention the company name naturally.
3. Clearly address the customer's concern.
4. Do not blame the customer.
5. Do not invent information, policies, refunds, or timelines.
6. The reply must not exceed the given maximum word limit.
7. Keep the response concise and relevant.
8. Return only the customer support reply.
9. Do not include headings, explanations, or extra text.
"""

customer_message = input("Enter customer message: ")

company_name = input("Enter company name: ")

max_words = input("Enter maximum words: ")

prompt = f"""
Customer Message:
{customer_message}

Company Name:
{company_name}

Maximum Words:
{max_words}

Write a professional customer support reply within the specified word limit.
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

print("\nSupport Reply:")
print(output)