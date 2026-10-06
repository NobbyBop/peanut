from .conversation import Conversation
from colorama import Fore
from ollama import generate
from .sessions import load_session, save_session
from .printing import print_peanut_nametag
from .tools import resolve_tools
import os

SYSTEM_PROMPT = f"""
you are peanut - a tiny agent harness in a loop.
only use plaintext, only lowercase.

you may think, call tools, and respond!
every message must be tagged at the beginning
1. <think>
2. <tool>
3. <respond>
the loop ends when you respond or if you forget to tag
"""
def harness_loop(session_id=""):
    conversation = []
    user_message = input("you > ")
    if user_message == "/exit":
        return
    conversation.append(f"user: {user_message}")
    while True:
        tools = resolve_tools()
        wants_tool=True
        interrupted=False
        while wants_tool:
            peanut_message = ""
            peanut_thinking = ""
            tool_calls = []
            wants_tool=False
            try:
                stream = invoke_harness(conversation, os.environ.get("MODEL") or "gemma4:e2b", tools.values(), True)
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

                    if chunk.message.tool_calls != None and chunk.message.tool_calls != []:
                        wants_tool=True
                        tool_calls += chunk.message.tool_calls

                conversation.add_peanut_message(peanut_message, peanut_thinking)

                for tool_call in tool_calls:
                    print("-")
                    print(Fore.YELLOW+f"[tool call ({tool_call.function.name})]"+Fore.RESET)
                    try:
                        result = tools[tool_call.function.name](**tool_call.function.arguments)
                        print(Fore.YELLOW+f"[result ({tool_call.function.name})] > "+Fore.RESET+ str(result))
                    except TypeError as e:
                        result = e
                    conversation.add_tool(tool_call.function.name, tool_call.function.arguments, result)

            except KeyboardInterrupt:
                interrupted = True
                break
                            
        if interrupted:
            conversation.add_user_message('[the user sent a keyboard interrupt, your response was cut off]')
            print("\n\n"+Fore.YELLOW+f">you interrupted peanut<"+Fore.RESET, end="")

        print("\n-")
        user_message = input("you > ")
        if user_message == "/exit":
            break
        while user_message == "/convo":
            print(conversation.get_messages())
            user_message = input("you > ")

        conversation.add_user_message(user_message)
    save_session(conversation.get_messages(), id=session_id)

# def harness_loop(session_id=""):
#     conversation = Conversation() 
#     if session_id != "":
#         session = load_session(session_id)
#         conversation.add_session(session)
#     else:
#         conversation.add_system_message(SYSTEM_PROMPT)
#     user_message = input("you > ")
#     if user_message == "/exit":
#         return
#     conversation.add_user_message(user_message)
#     while True:
#         tools = resolve_tools()
#         wants_tool=True
#         interrupted=False
#         while wants_tool:
#             peanut_message = ""
#             peanut_thinking = ""
#             tool_calls = []
#             wants_tool=False
#             try:
#                 stream = invoke_harness(conversation, os.environ.get("MODEL") or "gemma4:e2b", tools.values(), True)
#                 peanut_started_talking = False
#                 peanut_started_thinking = False
                
#                 for chunk in stream:
#                     if chunk.message.thinking != None and chunk.message.thinking != "":
#                         if not peanut_started_thinking:
#                             peanut_started_thinking = True
#                             print("-")
#                             print(Fore.YELLOW+"(thinking) > "+Fore.RESET, end="")
#                         print(Fore.LIGHTBLACK_EX, chunk.message.thinking, Fore.RESET, end='', sep='', flush=True)
#                         peanut_thinking += chunk.message.thinking or ""

#                     elif chunk.message.content != None and chunk.message.content != "":
#                         if not peanut_started_talking:
#                             peanut_started_talking = True
#                             print("-")
#                             print_peanut_nametag()
#                         print(chunk.message.content, end='', flush=True)
#                         peanut_message += chunk.message.content or ""

#                     if chunk.message.tool_calls != None and chunk.message.tool_calls != []:
#                         wants_tool=True
#                         tool_calls += chunk.message.tool_calls

#                 conversation.add_peanut_message(peanut_message, peanut_thinking)

#                 for tool_call in tool_calls:
#                     print("-")
#                     print(Fore.YELLOW+f"[tool call ({tool_call.function.name})]"+Fore.RESET)
#                     try:
#                         result = tools[tool_call.function.name](**tool_call.function.arguments)
#                         print(Fore.YELLOW+f"[result ({tool_call.function.name})] > "+Fore.RESET+ str(result))
#                     except TypeError as e:
#                         result = e
#                     conversation.add_tool(tool_call.function.name, tool_call.function.arguments, result)

#             except KeyboardInterrupt:
#                 interrupted = True
#                 break
                            
#         if interrupted:
#             conversation.add_user_message('[the user sent a keyboard interrupt, your response was cut off]')
#             print("\n\n"+Fore.YELLOW+f">you interrupted peanut<"+Fore.RESET, end="")

#         print("\n-")
#         user_message = input("you > ")
#         if user_message == "/exit":
#             break
#         while user_message == "/convo":
#             print(conversation.get_messages())
#             user_message = input("you > ")

#         conversation.add_user_message(user_message)
#     save_session(conversation.get_messages(), id=session_id)

# def invoke_harness(conversation,
#                    model=os.environ.get("MODEL") or "gemma4:e2b"):
#     stream = (
#         model=model,
#         prompt=conversation.get_messages(),
#         stream=True,
#     )
#     return stream

def invoke_harness(text, model):
    stream = generate(model, text)