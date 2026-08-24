import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)

REVIEW_CLASSIFIER_PROMPT = """
You are a customer review classifier.
Here are some exmples of customer reviews and their corresponding categories:
1. "The product quality is excellent and exceeded my expectations." - Category: Positive
2. "The delivery was delayed and the packaging was damaged." - Category: Negative
3. "The customer service was helpful and resolved my issue quickly." - Category: Positive
Please classify the following customer review into one of the following categories: Positive, Negative, or Neutral category. Only respond with the category name.
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