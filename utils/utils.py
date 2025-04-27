from dotenv import dotenv_values, find_dotenv

def get_env_vars():
    try:
        env_vars = dotenv_values(find_dotenv())

        return env_vars
    except FileNotFoundError:
        print("ENV FILE NOT FOUND")