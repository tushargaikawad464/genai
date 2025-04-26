from dotenv import dotenv_values

def get_env_vars():
    try:
        env_vars = dotenv_values("./.env")
        return env_vars
    except FileNotFoundError:
        print("ENV FILE NOT FOUND")

