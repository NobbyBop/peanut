from .conversation import Conversation
from colorama import Fore
from ollama import chat
from dotenv import load_dotenv
import os

SYSTEM_PROMPT = f"""
You are Peanut - a tiny agent harness.
Only use plaintext, only lowercase.
"""

def harness():
    load_dotenv()

    user_message = input(Fore.RESET+"you > ")
    conversation = Conversation()
    conversation.add_message('user', SYSTEM_PROMPT)
    conversation.add_message('user', user_message)
    while user_message != "/exit":
        stream = chat(
            model=os.environ.get("MODEL") or "gemma4:e2b",
            messages=conversation.get_messages(),
            think=False,
            stream=True
        )
        print("-")
        print(Fore.YELLOW + f"peanut > ", end="")
        peanut_message = ""
        for chunk in stream:
            print(Fore.RESET+chunk['message']['content'], end='', flush=True)
            peanut_message+=chunk['message']['content']
        conversation.add_message('assistant', peanut_message)
        print("\n-")
        user_message = input(Fore.RESET+"you > ")
        conversation.add_message('user', user_message)
    print("-\n"+Fore.YELLOW + f"peanut > " + Fore.RESET+"goodbye!\n")
    