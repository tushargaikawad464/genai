import os

def read_file(file_name, file_path):
    file_loc = os.path.join(file_path, file_name)

    if not os.path.exists(file_loc):
        return f"Error: The file '{file_loc}' does not exist.", "error"
    
    try:
        with open(file_loc, 'r') as file:
            content = file.read()
        return content, "success"
    except Exception as e:
        return f"Error reading file '{file_loc}': {e}", "error"

    
def write_file(file_path, content):
    try:
        with open(file_path, "w") as file:
            file.write(content)
        return f"writing to file successful", "success"
    except Exception as e:
        return f"Error writing to file '{file_path}': {e}", "error"
