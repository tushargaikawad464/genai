from dotenv import dotenv_values, find_dotenv

def get_env_vars():
    try:
        env_vars = dotenv_values(find_dotenv(".env.us-east-1"))

        return env_vars
    except FileNotFoundError:
        print("ENV FILE NOT FOUND")