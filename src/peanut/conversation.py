class Conversation:

    def __init__(self):
        self.messages = []

    def add_message(self, role, text):
        self.messages += [
            {
                'role':role,
                'content':text
            }
        ]

    def get_messages(self):
        return self.messages
