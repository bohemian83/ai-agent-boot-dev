import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)


def get_files_info(working_directory, directory="."):
    target_path = os.path.abspath(os.path.join(working_directory, directory))
    working_path = os.path.abspath(working_directory)

    if not target_path.startswith(working_path):
        return f'\tError: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(target_path):
        return f'\tError: "{directory}" is not a directory'

    try:
        items = os.listdir(target_path)
    except PermissionError:
        return f'\tError: Permission denied accessing directory "{directory}"'
    except FileNotFoundError:
        return f'\tError: Directory "{directory}" not found'
    except OSError as e:
        return f'\tError: Cannot access directory "{directory}": {e}'

    output_string = ""
    for item in items:
        abs_item_path = os.path.abspath(os.path.join(target_path, item))
        try:
            file_size = os.path.getsize(abs_item_path)
            is_directory = os.path.isdir(abs_item_path)
            output_string += (
                f" - {item}: file_size={file_size}, is_dir={is_directory}\n"
            )
        except (FileNotFoundError, PermissionError, OSError) as e:
            return f"\tError: {e}"

    return output_string
