from colorama import Fore
import subprocess
import os

def clear_screen():
    if os.name == "nt":
        subprocess.run(["cls"], shell=True)
    else:
        subprocess.run(["clear"])

def print_title(message):
    clear_screen()
    print(Fore.YELLOW + f"""
hi, i'm
                                             888        
                                             888        
                                             888        
88888b.   .d88b.   8888b.  88888b.  888  888 888888     
888 "88b d8P  Y8b     "88b 888 "88b 888  888 888        
888  888 88888888 .d888888 888  888 888  888 888        
888 d88P Y8b.     888  888 888  888 Y88b 888 Y88b.  d8b 
88888P"   "Y8888  "Y888888 888  888  "Y88888  "Y888 Y8P 
888                                                     
888                                                     
888                                                             

{message}
"""+Fore.RESET)

def print_heading(message):
        print(Fore.YELLOW+f"\n=== {message.lower()} ===\n"+Fore.RESET)

def print_goodbye():
    print("-\n"+Fore.YELLOW + f"peanut > " + Fore.RESET+"goodbye!\n")

def print_peanut_nametag(message=""):
    if message == "":
        print("-\n"+Fore.YELLOW + f"peanut > " + Fore.RESET, end="")
    else:
        print("-\n"+Fore.YELLOW + f"peanut > " + Fore.RESET + message + "\n-")