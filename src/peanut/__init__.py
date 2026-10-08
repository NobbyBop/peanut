from dotenv import load_dotenv
load_dotenv()

# from .menu import main_menu
from .harness import chat_loop

def main() -> None:
  chat_loop()

  
