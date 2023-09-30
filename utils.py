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

    # print("response", response)

    answer_match = re.search(r'ANSWER: "(.*?)"', response)
    thought_match = re.search(r'THOUGHT: "(.*?)"', response)
    
    answer = answer_match.group(1) if answer_match else None
    thought = thought_match.group(1) if thought_match else None
    
    # print("Answer:", answer)
    # print("Thought:", thought)
    
    return answer, thought

def extract_vote(text, names):
    for name in names:
        if name in text:
            return name
    return f"Error, no vote was recorded"