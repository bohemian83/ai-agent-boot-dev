from config import MAX_CHARS
from google.genai import types
import os

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets the content of the file specified in file path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file from which to get content from. If not provided, don't run the function.",
            ),
        },
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
            file_content_string = f.read(MAX_CHARS)
    except IOError as e:
        return f"\tError: Read failed: {e}"
    except Exception as e:
        return f"\tError: {e}"

    return file_content_string
