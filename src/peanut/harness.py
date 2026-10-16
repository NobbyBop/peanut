from .conversation import Conversation
from colorama import Fore
from ollama import chat, generate
from .sessions import load_session, save_session
from .printing import print_peanut_nametag
from .tools import resolve_tools
import os

SLIDING_WINDOW = 25

CHAT_SYSTEM_PROMPT = """you are 'peanut' - a tiny agent  in a loop.
only use plaintext, only lowercase.
<you>
conversation = load_conversation()
while True:
    conversation.add(get_user_message())
    response = peanut(conversation)
    if not response.startswith("[respond]") or not response.startswith("[tool]"):
        exit(1)
    if response.startswith("[respond]"):
        send_response_to_user(response)
    while response.startswith("[tool]"):
        result = execute_tool(response)
        conversation.add(result)
        peanut(conversation)
</you>
you will be given:

1. a list of tools you can call along with their definitions
2. a context summary
3. a message from a user OR a tool result from a tool you just called

you must do one, not both, of the following two things:
1. respond to the user - begin your message with "[respond]"
    - follow [respond] with the message you want the user to see, separated by a space
    - ex: "[respond] hey there"
2. call a tool from the list of tools - begin your message with "[tool]"
    - format: [tool] <tool_name> [array of args]
    - when you call a tool, the result will come back to you on the next turn before the user can see it.
    - ex: "[tool] add_two_numbers [4, 5]"

your goal is to respond to the user and call tools if/when necessary to respond
"""
def build_chat_prompt(conversation:Conversation, user_message:str, tools) -> str:
    print(tools)
    return ( f"""the tools you can call:
<tools>
{tools}
</tools>

the conversation:
<conversation>
{conversation.get_messages(SLIDING_WINDOW)}
</conversation>

the user message:
<user message>
{user_message}
</user message>
""" )

def harness_loop(session_id=""):
    conversation = Conversation() 
    if session_id != "":
        session = load_session(session_id)
        conversation.add_session(session)
    user_message = input("you > ")
    if user_message == "/exit":
        return
    conversation.add_user_message(user_message)
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
                prompt = build_chat_prompt(conversation, user_message, tools)
                stream = invoke_model(os.environ.get("MODEL", "llama3.1:8b"), prompt, CHAT_SYSTEM_PROMPT)
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

###


    
def chat_loop():
    conversation = Conversation()
    while True:
        user_message = input("you > ")
        conversation.add_user_message(user_message)
        prompt = build_chat_prompt(conversation, user_message)
        peanut_message = invoke_model(os.environ.get("MODEL", "llama3.1:8b"), prompt, CHAT_SYSTEM_PROMPT)
        print(f"peanut > {peanut_message}")
        conversation.add_peanut_message(peanut_message)

def invoke_model(model: str, prompt:str, system:str) -> str:
    resp = generate(model=model, system=system, prompt=prompt, stream=False)
    return resp.response or ""