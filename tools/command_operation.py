import subprocess


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
        return f"returncide: {exc.returncode}, Output: {exc.output}", "error"
    else:
        return f"Command Output: {output}", "success"