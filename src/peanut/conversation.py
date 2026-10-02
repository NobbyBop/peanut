class Conversation:

    def __init__(self):
        self.messages = []

    def add_message(self, role, content):
        self.messages += [
            {
                'role':role,
                'content':content
            }
        ]

    def add_session(self, session):
        for message in session:
            self.add_message(message['role'], message['content'])
    def get_messages(self):
        return self.messages
