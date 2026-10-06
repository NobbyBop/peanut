from ollama import chat
import os
def generate_session_title(messages):
    prompt = [
        {
            'role':'user',
            'content': f"""
you must create a title for this conversation with in no more than 5 words, all lowercase.
be quirky. all conversations are with peanut, only include peanut if conversation content is about peanut.
conversation:
{messages}
"""
        }
    ]
    response = chat(
        model=os.environ.get("MODEL") or "gemma4:e2b",
        messages=prompt,
        think=False,
        stream=False
    )
    return response["message"]["content"]

