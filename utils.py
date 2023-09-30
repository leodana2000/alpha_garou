import openai
import os
from dotenv import load_dotenv
import re

load_dotenv()

openai.api_key = os.environ.get("OPENAI_API_KEY")

async def api_call(text, ai):
    completion = openai.ChatCompletion.create(
        model=ai,
        messages=[
            {
                "role": "system",
                "content": text
            },
        ]
    )

    response = completion.choices[0].message.get("content", "")

    answer_thoughts = response.split("Thoughts:")

    answer = answer_thoughts[0]
    thought = answer_thoughts[1]

    return answer, answer + "\n Thoughts: " + thought

def extract_vote(text, names):
    for name in names:
        if name in text:
            return name
    raise "Error, no vote was recorded"