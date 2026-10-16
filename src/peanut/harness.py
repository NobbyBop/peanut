from .conversation import Conversation
# from colorama import Fore
from ollama import generate
# from .sessions import load_session, save_session
# from .printing import print_peanut_nametag
# from .tools import resolve_tools
import os
from itertools import islice

SLIDING_WINDOW = 25


SUMMARIZER_SYSTEM_PROMPT = """You are a context summarizer.
You will be given:
1. A pre-selected list of messages between a user and an agent named peanut.
2. A user message.

You will respond with a summary of knowledge from the message that peanut will use to respond.
Only report on what exists, do not mention lack of context."""
 
def build_summarizer_prompt(conversation:Conversation, user_message:str) -> str:
    return f"""The pre-selected list of messages:
<messages>
{conversation.to_str()}
</messages>

The user message:
<user message>
{user_message}
</user message>"""

def summarize_context(conversation:Conversation, user_message:str) -> str:
    prompt = build_summarizer_prompt(conversation, user_message)
    return invoke_model(os.environ.get("MODEL", "llama3.1:8b"), prompt, SUMMARIZER_SYSTEM_PROMPT)

# OPTIMIZER_SYSTEM_PROMPT = """You are a context optimizer. 
# You will be given:
# 1. A conversation between a user and an agent named peanut.
# 2. The user message which peanut will respond to next.
# 2. An evaluation message from the conversation to evaluate.

# You will respond strictly with:
# 'y' - the evaluation message is relevant
# 'n' - the evaluation message is irrelevant
# Any responses other than 'y' or 'n' will be rejected."""

# def build_optimizer_prompt(conversation:Conversation, user_message:str, index:int) -> str:
#     return f"""The conversation:
# <conversation>
# {conversation.to_str()}
# </conversation>

# The user message:
# <user message>
# {user_message}
# </user message>

# The evaluation message:
# <evaluation message>
# {conversation.get_messages()[index]}
# </evaluation message>"""

# def optimize_context(conversation:Conversation, user_message)-> Conversation:
#     conversation_messages = conversation.get_messages()
#     conversation_messages  = list(islice(reversed(conversation_messages), 0, SLIDING_WINDOW))
#     conversation_messages.reverse()
#     num_messages = len(conversation_messages)
#     if num_messages <= 1:
#         return conversation
#     optimized_conversation = Conversation()

#     ## Could do this concurrently...? Maybe.
#     for i in range(num_messages-1):
#         prompt = build_optimizer_prompt(conversation, user_message, i)
#         valid = invoke_model(os.environ.get("MODEL", "llama3.1:8b"), prompt, OPTIMIZER_SYSTEM_PROMPT)
#         if valid == 'y':
#             if conversation_messages[i]["role"] == "peanut":
#                 optimized_conversation.add_peanut_message(conversation_messages[i]["content"])
#             elif conversation_messages[i]["role"] == "peanut":
#                 optimized_conversation.add_user_message(conversation_messages[i]["content"])
#     return optimized_conversation

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
def build_chat_prompt(conversation:Conversation, user_message:str) -> str:
#     optimized_conversation = optimize_context(conversation, user_message)
#     print(f"""<optimized_conversation>
# {optimized_conversation.to_str()}
# </optimized_conversation>
# """)
    summarized_context = summarize_context(conversation, user_message)
    print(f"""<summarized_context>
{summarized_context}
</summarized_context>
""")
    return ( f"""the tools you can call:
<tools>
hit_endpoint
```
import requests
import json
def hit_endpoint(endpoint, method, body):
    if method == "POST":
        resp = requests.post(endpoint, data=json.loads(body))
        return resp
    elif method == "GET":
        resp = requests.get(endpoint, data=json.loads(body))
        return resp
    else:
        return "Invalid method."
```
</tools>

the context:
<context>
{summarized_context}
</context>

the user message:
<user message>
{user_message}
</user message>
""" )
    
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