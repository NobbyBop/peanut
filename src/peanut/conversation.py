from itertools import islice

ASSISTANT_NAME='assistant'
class Conversation:

    def __init__(self):
        self.messages = []

    def add_message(self, role, content):
        message = {
            'role':role,
            'content':content,
        }
        self.messages += [message]

    def add_session(self, session):
        for message in session:
            self.add_message(message.role, message.content)

    def get_messages(self, n=0):
        conversation_messages = self.messages
        if n > 0:
            conversation_messages  = list(islice(reversed(conversation_messages), 0, n))
            conversation_messages.reverse()
        return conversation_messages

    def to_str(self, n):
        convsersation_string = ""
        for message in self.get_messages(n):
            convsersation_string += f"{message['role']}> {message['content']}\n"
        return convsersation_string
