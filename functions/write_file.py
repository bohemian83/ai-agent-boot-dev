import os
from google.genai import types


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the content to the file specified in file path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to write to. If not provided, do not run the function.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content that is to be written to the provide file path.",
            ),
        },
    ),
)


def write_file(working_directory, file_path, content):
    target_path = os.path.abspath(os.path.join(working_directory, file_path))
    working_path = os.path.abspath(working_directory)

    if not target_path.startswith(working_path):
        return f'\tError: Cannot write to "{file_path}" as it is outside the permitted working directory'

    try:
        with open(target_path, "w") as f:
            f.write(content)
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except IOError as e:
        return f"\tError: Write failed: {e}"
    except Exception as e:
        return f"'\tError: {e}"
