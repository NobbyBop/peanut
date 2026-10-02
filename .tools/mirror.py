import os
def mirror() -> str:
    peanut_path = os.path.dirname(__file__)
    with open(peanut_path+"/__init__.py", 'r') as file:
        content = file.read()
        return content
