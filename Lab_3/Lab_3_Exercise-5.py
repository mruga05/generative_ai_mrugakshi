import os
import re
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)

SYSTEM_PROMPT = """
You are a multilingual translation assistant.

Read the given input carefully and translate it into the requested output language.

Rules:
1. Do not change the meaning of the input.
2. Do not add any information that is not present in the input.
3. Preserve the original tone and intent.
4. Return only the translated text.
5. Do not provide explanations.
"""

input_text = input("Enter text: ")
input_lang = input("Enter input language: ")
output_lang = input("Enter output language: ")

prompt = f"""
Input Language:
{input_lang}

Output Language:
{output_lang}

Text:
{input_text}

Translate the text from the input language to the output language.
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

print("\nTranslation:")
print(output)