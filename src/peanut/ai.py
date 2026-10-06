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


def test():
    prompt = [
        {
            'role':'joe',
            'content': """you should be able to see the conversation history between us, right? can you see my 'role' as well?
             messages are sent like this: 
             {
                'role':'role here',
                'content': 'string'
            }"""
        }
    ]
    response = chat(
        model=os.environ.get("MODEL") or "gemma4:e2b",
        messages=prompt,
        think=False,
        stream=False
    )
    return response["message"]["content"]
