from dotenv import load_dotenv
load_dotenv()

from .printing import print_title
from .harness import chat_loop, inline_loop
import sys
def print_usage():
    print("""usage:
peanut
peanut -t "natural language command" """)
def main():
    if len(sys.argv) == 1:
        print_title("send a message to get started")
        chat_loop()
        exit(0)
    elif len(sys.argv) == 3:
        if sys.argv[1] == "-t" and isinstance(sys.argv[2], str):
            chat_loop(inline=True, user_message=sys.argv[2])
            exit(0)

    print_usage()
    
    