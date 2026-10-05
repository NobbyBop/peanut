from dotenv import load_dotenv
load_dotenv()

from .menu import main_menu

from .sandbox import execute_tool
def main() -> None:
  # main_menu()
  execute_tool("echo", "test 1", "test 2")
  

  
