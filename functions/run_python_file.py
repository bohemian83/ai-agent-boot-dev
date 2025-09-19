import subprocess
import os
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns the output from the interpreter.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
                description="Optional arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)


def run_python_file(working_directory, file_path, args=[]):
    target_path = os.path.abspath(os.path.join(working_directory, file_path))
    working_path = os.path.abspath(working_directory)

    if not target_path.startswith(working_path):
        return f'\tError: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(target_path):
        return f'\tError: File "{file_path}" not found.'

    if not file_path.endswith(".py"):
        return f'\tError: "{file_path}" is not a Python file.'

    try:
        commands = ["python, target_path"]
        if args:
            # could also use commands.extend(args)
            commands = ["python", target_path, *args]
        completed_process = subprocess.run(
            commands,
            check=True,
            capture_output=True,
            timeout=30,
            text=True,
            cwd=target_path,
        )
        output = []
        if completed_process.stdout:
            output.append(f"STDOUT:\n{completed_process.stdout}")
        if completed_process.stderr:
            output.append(f"STDERR:\n{completed_process.stderr}")

        if completed_process.returncode != 0:
            output.append(f"Process exited with code {completed_process.returncode}")

        return "\n".join(output) if output else "No output produced."
    except Exception as e:
        return f"\tError: executing Python file {e}"
