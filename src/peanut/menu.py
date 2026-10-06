from .harness import harness_loop
from .printing import print_title, print_heading, print_peanut_nametag
from .sessions import get_list_sessions, get_session_title
from colorama import Fore

class Menu():

    def __init__(self, options: list):
        if len(options) < 1:
            raise ValueError("class menu - options cannot be empty")
        self.options=options
        self.selected = 0


    def _validate_selected(self, number):
        return number in range(1, len(self.options)+2)
    
    def display_options(self):
        count = 0
        for opt in self.options:
            print(Fore.YELLOW+f"{count+1}: "+Fore.RESET+f"{opt}")
            count+=1
        print()

    def set_selected(self, number):
        if self._validate_selected(number):
            self.selected = number-1
        else:
            raise IndexError("class menu - set_selected - number out of range")

    def get_selected(self):
        return self.selected+1
    
    def get_selected_option(self):
        return self.options[self.selected]

    def prompt_selection(self):
        user_input = 0
        while not self._validate_selected(user_input):
            try:
                user_input = int(input("you > "))
            except TypeError:
                print_heading("input out of range")
        return user_input

def session_menu() -> tuple[str, str]:
    while True:
            sessions = get_list_sessions()
            sessions.reverse()

            if len(sessions) == 0:
                print_heading("no sessions exist")
                return ("none", "none")
    
            print_title("sessions")
    
            titles = []
            count = 0
            for id in sessions:
                titles.append(get_session_title(id))
                count+=1
                if count > 4:
                    break

            sessions_menu = Menu(sessions[0:6]+["<go back>"])
            titles_menu = Menu(titles + ["<go back>"])

            titles_menu.display_options()
            option = titles_menu.prompt_selection()
            titles_menu.set_selected(option)
            title = titles_menu.get_selected_option()

            sessions_menu.set_selected(option)
            id = sessions_menu.get_selected_option()

            return (id, title)
            
def main_menu():
    option = "new session"
    status_update = ""
    while option != "exit":
        print_title("main menu")
        if status_update != "":
            print_heading(status_update)
        if len(get_list_sessions()) != 0:
            options = ["new session", "load session", "exit"]
        else:
            options = ["new session", "exit"]
        main_menu = Menu(options)
        main_menu.display_options()
        choice = main_menu.prompt_selection()
        main_menu.set_selected(choice)
        option = main_menu.get_selected_option()

        if option == "new session":
            print_title("new session")
            print_peanut_nametag(message="hi i'm peanut, what can i do you for?")
            harness_loop()
        elif option == "load session":
            tup = session_menu()
            id = tup[0]
            title = tup[1]
            if id == "none":
                status_update = "no sessions to load"
                continue
            if id == "<go back>":
                continue
            print_title(title)
            print_peanut_nametag(message="let's pick back up where we left off")
            harness_loop(session_id=id)
        else:
            continue
