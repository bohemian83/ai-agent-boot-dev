from config import MAX_CHARS
from google.genai import types
import os

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Reads and returns the first {MAX_CHARS} characters of the content from a specified file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file whose content should be read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)


def get_file_content(working_directory, file_path):
    target_path = os.path.abspath(os.path.join(working_directory, file_path))
    working_path = os.path.abspath(working_directory)

    if not target_path.startswith(working_path):
        return f"\tError: Cannot read {file_path} as it is outside the permitted working directory"

    if not os.path.isfile(target_path):
        return f'\tError: File not found or is not a regular file: "{file_path}"'

    try:
        with open(target_path, "r") as f:
            file_content = f.read(MAX_CHARS)
            if os.path.getsize(target_path) > MAX_CHARS:
                file_content += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )
        return file_content
    except IOError as e:
        return f"\tError: Read failed: {e}"
    except Exception as e:
        return f"\tError reading file '{file_path}': {e}"
