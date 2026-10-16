from itertools import islice

ASSISTANT_NAME='assistant'
class Conversation:

    def __init__(self):
        self.messages = []

    def _add_message(self, role, content, thinking="", tool_id=""):
        message = {
            'role':role,
            'content':content,
        }
        
        if thinking != "":
            message['thinking'] = thinking

        if tool_id != "":
            message['tool_id'] = tool_id
            
        self.messages += [message]

    def add_system_message(self, content):
            self._add_message('system', content)

    def add_user_message(self, content):
            self._add_message('user', content)

    def add_peanut_message(self, content, thinking=""):
        self._add_message(ASSISTANT_NAME, content, thinking=thinking)

    def add_tool(self, name, arguments, result):
        content = f"""
you just called 
tool: {name}
with arguments: {arguments}
the result was: {result}
"""
        self._add_message(ASSISTANT_NAME, content)
        
    def add_session(self, session):
        for message in session:
            self._add_message(message.role, message.content, message.thinking or "", message.tool_id or "")

    def get_messages(self, n=0):
        conversation_messages = self.messages
        if n > 0:
            conversation_messages  = list(islice(reversed(conversation_messages), 0, n))
            conversation_messages.reverse()
        return conversation_messages

    def to_str(self, n):
        convsersation_string = ""
        for message in self.get_messages(n):
            convsersation_string += f"{message['role']} > {message['content']}\n"
        return convsersation_string
