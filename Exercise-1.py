import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)

COLLEGE_CLUB_SYSTEM_PROMPT = """
You are a College Club Recommendation Assistant.

Your job is to recommend college clubs to students based on their interests, hobbies, skills, and personality.

Available college clubs:
- Coding Club
- AI/ML Club
- Robotics Club
- Photography Club
- Music Club
- Dance Club
- Sports Club
- Debate Club
- Entrepreneurship Club
- Literary Club
- Social Service Club

Ask the student questions about their interests, hobbies, skills, favorite subjects, and preferred activities.

After collecting enough information, recommend the top 3 most suitable clubs.

For each recommendation:
1. Give the club name.
2. Give a short reason why it matches the student's interests.
3. Give one activity the student could participate in.

Do not recommend clubs that are not in the available club list.

Be friendly, simple, and student-friendly.
"""
history = [{
    "role": "system",
    "content": COLLEGE_CLUB_SYSTEM_PROMPT
}]

while True:
    print("Enter your prompt:")
    prompt = input()

    if prompt.lower() == "exit":
        print("Goodbye!")
        break

    history.append({
        "role": "user",
        "content": prompt
    })

    chat_completion = client.chat.completions.create(
        messages=history,
        model="qwen/qwen3.6-27b"
    )

    output = chat_completion.choices[0].message.content

    print("Bot:", output)

    history.append({
        "role": "assistant",
        "content": output
    })