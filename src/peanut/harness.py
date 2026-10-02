from .conversation import Conversation
from colorama import Fore
from ollama import chat
from .sessions import load_session, save_session
import os

SYSTEM_PROMPT = f"""
you are peanut - a tiny agent harness.
only use plaintext, only lowercase.
"""

def harness_loop(session_id=""):
    conversation = Conversation() 
    if session_id != "":
        session = load_session(session_id)
        conversation.add_session(session)
    else:
        conversation.add_message('user', SYSTEM_PROMPT)
    user_message = input("you > ")
    if user_message == "/exit":
        return
    conversation.add_message('user', user_message)
    while True:
        stream = invoke_harness(conversation, user_message, os.environ.get("MODEL") or "gemma4:e2b")
        print("-")
        print(Fore.YELLOW + f"peanut > "+Fore.RESET, end="")
        peanut_message = ""
        for chunk in stream:
            print(chunk['message']['content'], end='', flush=True)
            peanut_message+=chunk['message']['content']
        conversation.add_message('assistant', peanut_message)
        print("\n-")
        user_message = input("you > ")
        if user_message == "/exit":
            break
        conversation.add_message('user', user_message)
    save_session(conversation.get_messages(), id=session_id)

def invoke_harness(conversation, user_message, model):
    conversation.add_message('user', user_message)
    stream = chat(
        model=model,
        messages=conversation.get_messages(),
        think=False,
        stream=True
    )
    return stream