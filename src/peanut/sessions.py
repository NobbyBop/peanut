from dotenv import load_dotenv
import os
import json
import uuid

def load_session(id:str):
    load_dotenv()
    sessions_path = os.environ.get("SESSIONS_DIR") or "~/.peanut/.sessions"
    try:
        with open(sessions_path+f"{id}.json", "r") as file:
            content = file.read()
            conversation = json.loads(content)
    except:
        raise KeyError(f"Session with ID {id} does not exist")

def save_session(conversation):
    id = uuid.uuid4()
    load_dotenv()
    sessions_path = os.environ.get("SESSIONS_DIR") or "~/.peanut/.sessions"
    with open(sessions_path+f"{id}.json", "w") as file:
        content = file.write(json.dumps(conversation))
    return id
 