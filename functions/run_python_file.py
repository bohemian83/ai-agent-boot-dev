import subprocess
import sys
import os


def run_python_file(working_directory, file_path, args=[]):
    target_path = os.path.abspath(os.path.join(working_directory, file_path))
    working_path = os.path.abspath(working_directory)

    if not target_path.startswith(working_path):
        return f'\tError: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(target_path):
        return f'\tError: File "{file_path}" not found.'

    if target_path[-2:] != "py":
        return f'\tError: "{file_path}" is not a Python file.'

    try:
        completed_process = subprocess.run(
            ["python", target_path, *args], check=True, capture_output=True, timeout=30
        )
    except Exception as e:
        return f"\tError: executing Python file {e}"

    if completed_process.returncode == 0:
        return f"STDOUT: {completed_process.stdout}\nSTDERR: {completed_process.stderr}"
    elif completed_process is None:
        return "No output produced"
    else:
        return f"Process exited with code {completed_process.returncode}"
