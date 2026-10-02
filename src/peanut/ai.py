from ollama import chat
import os
def generate_session_title(messages):
    prompt = [
        {
            'role':'user',
            'content': f"""
You must create a title for this conversation in no more than 5 words, all lowercase.
Conversation:
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
