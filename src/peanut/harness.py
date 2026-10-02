from .conversation import Conversation
from colorama import Fore
from ollama import chat
from .sessions import load_session, save_session
import os

SYSTEM_PROMPT = f"""
You are Peanut - a tiny agent harness.
Only use plaintext, only lowercase.
"""

def harness(session_id):
    conversation = Conversation() 
    if session_id != "":
        session = load_session(session_id)
        conversation.add_session(session)
    else:
        conversation.add_message('user', SYSTEM_PROMPT)

    user_message = input("you > ")
    conversation.add_message('user', user_message)

    while True:
        stream = chat(
            model=os.environ.get("MODEL") or "gemma4:e2b",
            messages=conversation.get_messages(),
            think=False,
            stream=True
        )
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

    print("-\n"+Fore.YELLOW + f"peanut > " + Fore.RESET+"goodbye!\n")
    save_session(conversation.get_messages(), id=session_id)
    