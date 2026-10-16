from .conversation import Conversation
from colorama import Fore
from ollama import chat, generate
from .sessions import load_session, save_session
from .printing import print_peanut_nametag
import os


SLIDING_WINDOW = 25

CHAT_SYSTEM_PROMPT = """you are 'peanut' - a tiny agent in a loop.
only use plaintext, only lowercase.

you will be given:
1. conversation history
    - messages from 'peanut' are what you have said or actions you have taken
    - messages from 'user' are what the user has said
    - messages from 'server' are results from the server that you have caused
    - messages from 'system' will inform you about malformed responses, etc.

your goal:
    - respond to the most recent user message
    - messages after the user message means either the system or server has responded to you

you must do one of the following two things to respond to the user's message:
1. respond directly - begin your message with "[respond]"
    - follow [respond] with the message you want the user to see, separated by a space
    - ex: "[respond] hey there user"
2. get data from the remote server - your entire message should be "[get]"
    - ex: "[get]"
    - note: you will receive a 'server' message with the data, or receive a failure.
3. post data to the remote server - begin your message with "[post]"
    - ex: "[post] hello server"
    - note: the user cannot see the remote server
    - note: you will receive a success/fail message from the server after doing this

critical: any response that does not begin with [respond], [get], or [post] will be rejected and the loop will crash.
"""

def build_chat_prompt(conversation:Conversation) -> str:
    return ( f"""the conversation:
<conversation>
{conversation.to_str(SLIDING_WINDOW)}
</conversation>
""" )

def parse_model_response(response:str):
    if not response.startswith("["):
        raise ValueError("Response is invalid. Does not start with '['")
    idx = response.find(']')
    if idx == -1:
        raise ValueError("Response is invalid. Does not close '[' with ']'")
    action = response[1:idx]
    if action not in ["respond", "get", "post"]:
        raise ValueError("Response is invalid. Action must be either 'respond', 'get', or 'post'")
    return {
        "action":action,
        "body": response[idx+1:]
        }

def harness_loop(session_id=""):
    conversation = Conversation() 
    if session_id != "":
        session = load_session(session_id)
        conversation.add_session(session)
    user_message = input("you > ")
    if user_message == "/exit":
        return
    conversation.add_message('user', user_message)
    while True:
        prompt = build_chat_prompt(conversation)
        raw_response = invoke_model(os.environ.get("MODEL", "gemma4:e2b"), prompt, CHAT_SYSTEM_PROMPT)
        print("raw:", raw_response)
        response = parse_model_response(raw_response)

        while response["action"] == "get" or response["action"] == "post":
            if response["action"] == "get":
                conversation.add_message('peanut', raw_response)
                conversation.add_message('server', 'data: {"number":42}')
            else:
                conversation.add_message('peanut', raw_response)
                conversation.add_message('server', 'data: {"success":"true"}')
            prompt = build_chat_prompt(conversation)
            raw_response = invoke_model(os.environ.get("MODEL", "gemma4:e2b"), prompt, CHAT_SYSTEM_PROMPT)
            response = parse_model_response(raw_response)
            
        conversation.add_message('peanut', response)
        print_peanut_nametag(response["body"])
        user_message = input("you > ")
        if user_message == "/exit":
            break
        conversation.add_message('user', user_message)
    save_session(conversation.get_messages(), id=session_id)


def invoke_model(model: str, prompt:str, system:str) -> str:
    resp = generate(model=model, system=system, prompt=prompt, stream=False, think=True)
    return resp.response or ""