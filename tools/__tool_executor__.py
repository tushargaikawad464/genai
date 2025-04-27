import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.utils import get_env_vars
from tools.command_operation import run_cli_commands
from tools.file_operation import read_file, write_file

env_vars = get_env_vars()

def execute_tools(func_name, func_input=None):
    try:
        if func_name not in globals():
            return f"Function '{func_name}' is not definded", "error"
        
        func = globals()[func_name]

        if func_input:
            print(f"Executing Action {func_name}, Action Input: {func_input}")
            result = func(**func_input)
        else:
            print(f"Executing Action {func_name}")
            result = func(**func_input)

        return result
    
    except Exception as e:
        return f"Error while executing function call '{func_name}' ERROR: {e}"
    

# result, status = execute_tools("run_cli_commands", "unsame -a")
    