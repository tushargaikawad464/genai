import subprocess

def execute_tools(func_name, func_input=None):
    try:
        if func_name not in globals():
            return f"Function '{func_name}' is not definded"
        
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

def run_cli_commands(command):
    try:
        output = subprocess.check_output(
            command,
            stderr=subprocess.STDOUT,
            shell=True,
            timeout=5,
            universal_newlines=True
        )
    except subprocess.CalledProcessError as exc:
        return f"Command Status: FAIL, returncide: {exc.returncode}, Output: {exc.output}"
    else:
        return f"Command Output: {output}"


