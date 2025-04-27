def read_file(file_path):

    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    except Exception as e:
        return "Error reading file '{file_path}': {e}"
    
def write_file(file_path, content):
    try:
        with open(file_path, "w") as file:
            file.write(content)
        return f"writing to file successful"
    except Exception as e:
        return f"Error writing to file '{file_path}': {e}"
