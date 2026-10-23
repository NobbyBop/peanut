from .conversation import Conversation
from ollama import generate
from .printing import print_peanut_nametag, print_peanut_command
import os
from pydantic import BaseModel
from enum import Enum
import json
import subprocess


class Action(Enum):
    respond = "respond"
    execute = "command"
    
class ResponseFormat(BaseModel):
    action: Action
    message: str | None
    command: str | None

SLIDING_WINDOW = 25
MAX_ATTEMPTS = 3

CHAT_SYSTEM_PROMPT = """you are 'peanut' - a tiny agent who works on the user's windows computer
only use plaintext, only lowercase

you will be given:
1. conversation history
    - messages from 'peanut' are what you have said or powershell commands you have run
    - messages from 'user' are what the user has said
    - messages from 'system' will inform you of command outputs

your goal:
    - handle the most recent user message
        - execute commands until the request has been addressed
            - note: be persistent, don't give up after one failed command
        - otherwise, respond to the user to report the result

you must do one of the following two things to respond to the user's message:
1. respond directly - choose the "respond" action
    - set the "message" to the message you want the user to see
    - ex: {"action": "respond", "message":"hey there user"}
2. run a command - choose the "command" action
    - set the "command" to the windows powershell command you want to run
    - ex: {"action": "command", "command":"dir"}
    - note: "command" must be a valid powershell command, it will be run verbatim in the terminal

critical: your response must be a valid json object of the described schema and nothing else
"""

def build_chat_prompt(conversation:Conversation) -> str:
    return ( f"""the conversation:
<conversation>
{conversation.to_str(SLIDING_WINDOW)}
</conversation>
""" )

def harness_loop():
    conversation = Conversation() 
    while True:
        user_message = input("you > ")
        conversation.add_message('user', user_message)
        prompt = build_chat_prompt(conversation)

        response = {}

        for i in range(MAX_ATTEMPTS):
            try:
                response = json.loads(invoke_model(prompt))
                break
            except json.decoder.JSONDecodeError:
                if i == MAX_ATTEMPTS-1:
                    print("peanut is having trouble, try again later.")
                    exit(1)

                conversation.add_message('system', 'error')
        while response['action'] == 'command':
            print_peanut_command(response['command'])
            print(f"peanut wants to run the following command: {response['command']}")
            conversation.add_message('peanut', {response['command']})
            approval = input("allow? [y/n] > ")
            if approval == 'y':
                result = subprocess.run(response['command'].split(" "), shell=True, capture_output=True, text=True)
                conversation.add_message('system', result)
            else:
                conversation.add_message('system', "the user denied you permission to run the command. follow up with them.")
            prompt = build_chat_prompt(conversation)

            for i in range(MAX_ATTEMPTS):
                try:
                    response = json.loads(invoke_model(prompt))
                    break
                except json.decoder.JSONDecodeError:
                    if i == MAX_ATTEMPTS-1:
                        print("peanut is having trouble, try again later.")
                        exit(1)

        conversation.add_message('peanut', response['message'])
        print_peanut_nametag(response['message'])

def invoke_model(prompt:str) -> str:
    resp = generate(model=os.environ.get('MODEL', 'gemma4:e2b'), system=CHAT_SYSTEM_PROMPT, prompt=prompt)
    return resp.response or "{}"