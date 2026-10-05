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
