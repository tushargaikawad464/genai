import yaml


def load_yaml(path):
    with open(path, "r") as file:
        content = yaml.safe_load(file)
    return content


def get_prompt(prompt_path):
    return load_yaml(prompt_path)