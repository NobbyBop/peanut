import os
import json
from datetime import datetime
from .ai import generate_session_title

"""
Sessions are given ids of the current time at save. Re-saving a session keeps original date.
Format of one session is:
{
    "title":"Example Title",
    "messages":[
        {
            'role':'user',
            'content':"blah blah blah"
        },
        etc...  
    ]
}
"""
def load_session(id:str):
    sessions_path = os.environ.get("SESSIONS_DIR") or "~/.peanut/.sessions"
    try:
        with open(os.path.join(sessions_path, f"{id}"), "r") as file:
            content = file.read()
            data = json.loads(content)
            return data["messages"]
    except:
        raise KeyError(f"Session with ID {id} does not exist")

def save_session(messages, id=""):
    if id == "":
        id = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    title = generate_session_title(messages)
    sessions_path = os.environ.get("SESSIONS_DIR") or "~/.peanut/.sessions"
    with open(os.path.join(sessions_path, f"{id}"), "w") as file:
        session_json = {
            "title":title,
            "messages":messages
        }
        file.write(json.dumps(session_json))
    return id

def get_list_sessions():
    sessions_path = os.environ.get("SESSIONS_DIR") or "~/.peanut/.sessions"
    return os.listdir(sessions_path)

def get_session_title(id):
    sessions_path = os.environ.get("SESSIONS_DIR") or "~/.peanut/.sessions"
    try:
        with open(os.path.join(sessions_path, f"{id}"), "r") as file:
            content = file.read()
            data = json.loads(content)
            return data["title"]
    except:
        raise KeyError(f"Session with ID {id} does not exist")