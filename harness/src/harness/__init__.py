from dotenv import load_dotenv
load_dotenv()

from .printing import print_title
from .harness import harness_loop

def main() -> None:
  print_title("send a message to get started")
  harness_loop()
