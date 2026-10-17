from .conversation import Conversation
from ollama import generate
from .printing import print_peanut_nametag, print_peanut_tool
import os
from pydantic import BaseModel
from enum import Enum
import json

class Action(Enum):
    respond = "respond"
    get = "get"
    post = "post"

class ResponseFormat(BaseModel):
    action: Action
    message: str | None
    body: dict | None

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
1. respond directly - choose the "respond" action
    - set the "message" to the message you want the user to see
    - ex: {"action": "respond", "message":"hey there user"}
2. get data from the remote server - choose the "get" action
    - leave all fields blank
    - ex: {"action": "get"}
    - note: you will receive a 'server' message with the data, or receive a failure.
3. post data to the remote server - choose the "post" action
    - set the "body" to the json payload you want to post
    - ex: {"action": "post", "body":<data here>}
    - note: you will receive a success/fail message from the server after doing this
"""

def build_chat_prompt(conversation:Conversation) -> str:
    return ( f"""the conversation:
<conversation>
{conversation.to_str(SLIDING_WINDOW)}
</conversation>
""" )

def harness_loop():
    conversation = Conversation() 
    user_message = input("you > ")
    if user_message == "/exit":
        return
    conversation.add_message('user', user_message)
    while True:
        prompt = build_chat_prompt(conversation)
        response = json.loads(invoke_model(os.environ.get("MODEL", "gemma4:e2b"), prompt, CHAT_SYSTEM_PROMPT))
        while response["action"] == "get" or response["action"] == "post":
            print_peanut_tool(response["action"])
            if response["action"] == "get":
                conversation.add_message('peanut', response)
                conversation.add_message('server', 'data: {"number":42}')
            else:
                conversation.add_message('peanut', response)
                conversation.add_message('server', 'data: {"success":"true"}')
            prompt = build_chat_prompt(conversation)
            response = json.loads(invoke_model(os.environ.get("MODEL", "gemma4:e2b"), prompt, CHAT_SYSTEM_PROMPT))
        conversation.add_message('peanut', response["message"])
        print_peanut_nametag(response["message"])
        user_message = input("you > ")
        if user_message == "/exit":
            break
        conversation.add_message('user', user_message)

def invoke_model(model: str, prompt:str, system:str) -> str:
    resp = generate(model=model, system=system, prompt=prompt)
    return resp.response or "{}"