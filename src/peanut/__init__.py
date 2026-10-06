# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "colorama>=0.4.6",
#     "ollama>=0.6.3",
#     "python-dotenv>=1.2.4",
# ]
# ///
from dotenv import load_dotenv
load_dotenv()

from .menu import main_menu

# from .tools import execute_tool, resolve_tools
def main() -> None:
  main_menu()  

  
