import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)

REVIEW_CLASSIFIER_PROMPT = """
You are a customer review classifier.

Classify the given customer review into exactly one of these categories:

Positive:
The customer is satisfied, happy, or praises the product or service.

Negative:
The customer is dissatisfied, unhappy, or complains about the product or service.

Neutral:
The review is mainly factual or does not clearly express positive or negative sentiment.

Mixed:
The review contains both significant positive and negative opinions.

Rules:
1. Return only one category label.
2. The output must be exactly one of:
   Positive
   Negative
   Neutral
   Mixed
3. Do not provide explanations.
4. Do not add punctuation or extra text.
"""

review_text = input("Enter customer review: ")

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": REVIEW_CLASSIFIER_PROMPT
        },
        {
            "role": "user",
            "content": review_text
        }
    ],
    model="qwen/qwen3.6-27b"
)

output = chat_completion.choices[0].message.content.strip()

print("Category:", output)