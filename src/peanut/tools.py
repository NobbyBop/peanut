from pathlib import Path
import importlib
import sys
import os

tools_path = os.environ.get("TOOLS_DIR") or "~/.peanut/.tools/"
sys.path.insert(0, tools_path)

def execute_tool(tool, *args):
    module_name = tool
    module = importlib.import_module(module_name)
    module.__getattribute__(tool)(*args)

def resolve_tools():
    importlib.invalidate_caches()
    module_names = os.listdir(tools_path)
    module_names = list(filter(lambda x: ".py" in x, module_names))
    module_names = list(map(lambda x: x.strip(".py"), module_names))
    tools = {}
    for module_name in module_names:
        module = importlib.import_module(module_name)
        tools[module_name]=module.__getattribute__(module_name)
    return tools
        
