import os
from google.genai import types


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file within the working directory. Creates the file if it doesn't exist.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file",
            ),
        },
        required=["file_path", "content"],
    ),
)


def write_file(working_directory, file_path, content):
    target_path = os.path.abspath(os.path.join(working_directory, file_path))
    working_path = os.path.abspath(working_directory)

    if not target_path.startswith(working_path):
        return f'\tError: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(target_path):
        try:
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
        except Exception as e:
            return f"Error: creating directory: {e}"

    if os.path.exists(target_path) and os.path.isdir(target_path):
        return f'Error: "{file_path}" is a directory, not a file'

    try:
        with open(target_path, "w") as f:
            f.write(content)
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except IOError as e:
        return f"\tError: Write failed: {e}"
    except Exception as e:
        return f"'\tError writing to file '{file_path}': {e}"
