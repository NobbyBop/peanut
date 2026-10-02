from dotenv import load_dotenv
load_dotenv()

from .harness import harness
from .welcome import print_welcome
from .sessions import get_list_sessions, get_session_title
from colorama import Fore

def main() -> None:
  while True:
    print_welcome()

    sessions = get_list_sessions()
    sessions.reverse()

    if len(sessions) == 0:
      print(Fore.YELLOW+"let me know what i can help you with\n"+Fore.RESET)
      harness("")
      continue

    print(Fore.YELLOW+"want to pick back up?\n"+Fore.RESET)

    sessions_to_titles = []
    count = 0
    for id in sessions:
      title = get_session_title(id)
      sessions_to_titles.append((count, title, id))
      print(Fore.YELLOW+f"{count+1}: "+Fore.RESET+f"{title}")
      count+=1
      if count > 4:
        break

    number = input("\nload # (or skip w/ enter) > ")
    if number == "/exit":
      break
    if number == "":
      print(Fore.YELLOW+"\n=== STARTING NEW SESSION ===\n"+Fore.RESET)
      harness("")
      continue
    try:
      number = int(number)
    except:
      number = 0
    if number > 5 or number < 1 or number < len(sessions):
      print(Fore.YELLOW+"\n=== FAILED TO LOAD SESSION, STARTING NEW SESSION ===\n"+Fore.RESET)
      session_id = ""
    else:
      session_id = sessions_to_titles[number-1][2]
    print(Fore.YELLOW+"\n=== LOADED SESSION ===\n"+Fore.RESET)
    harness(session_id)
    continue
    

  

  
