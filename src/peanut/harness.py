from .conversation import Conversation
from colorama import Fore
from ollama import chat
from .sessions import load_session, save_session
from .printing import print_peanut_nametag
from .tools import resolve_tools
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
        tools = resolve_tools()
        tool_call=True

        while tool_call:
            peanut_message = ""
            peanut_thinking = ""
            tool_call=False
            stream = invoke_harness(conversation, os.environ.get("MODEL") or "gemma4:e2b", tools.values())
            peanut_started_talking = False
            peanut_started_thinking = False
            
            for chunk in stream:

                if chunk.message.thinking != None and chunk.message.thinking != "":
                    if not peanut_started_thinking:
                        peanut_started_thinking = True
                        print("-")
                        print(Fore.YELLOW+"(thinking) > "+Fore.RESET, end="")
                    print(Fore.LIGHTBLACK_EX, chunk.message.thinking, Fore.RESET, end='', sep='', flush=True)
                    peanut_thinking += chunk.message.thinking or ""

                elif chunk.message.content != None and chunk.message.content != "":
                    if not peanut_started_talking:
                        peanut_started_talking = True
                        print("-")
                        print_peanut_nametag()
                    print(chunk.message.content, end='', flush=True)
                    peanut_message += chunk.message.content or ""

                if chunk.message.tool_calls:
                    tool_call=True
                    for tool_call in chunk.message.tool_calls:
                        print("-")
                        print(Fore.YELLOW+f"[tool call ({tool_call.function.name})] > "+Fore.RESET, end="")
                        result = tools[tool_call.function.name](**tool_call.function.arguments)
                        conversation.add_tool(tool_call.function.name, result)
                        # print(Fore.YELLOW+"[result] > "+Fore.RESET, result, end="")

            if peanut_thinking != "":
                conversation.add_message('thinking', peanut_thinking)
            if peanut_message != "":
                conversation.add_message('assistant', peanut_message)

        print("\n-")
        user_message = input("you > ")
        if user_message == "/exit":
            break
        conversation.add_message('user', user_message)
    save_session(conversation.get_messages(), id=session_id)

def invoke_harness(conversation,
                   model=os.environ.get("MODEL") or "gemma4:e2b", 
                   tools=[], 
                   think=False):
    stream = chat(
        model=model,
        messages=conversation.get_messages(),
        think=True,
        stream=True,
        tools=tools
    )
    return stream

"""
invoke harness:
    stream = chat(...)
    for chunk in stream:
        if chunk.tool:
            tool.execute()
            conversation.append(tool.result)
"""