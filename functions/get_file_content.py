from config import MAX_CHARS
import os


def get_file_content(working_directory, file_path):
    target_path = os.path.abspath(os.path.join(working_directory, file_path))
    working_path = os.path.abspath(working_directory)

    if not target_path.startswith(working_path):
        return f"\tError: Cannot read {file_path} as it is outside the permitted working directory"

    if not os.path.isfile(target_path):
        return f'\tError: File not found or is not a regular file: "{file_path}"'

    with open(target_path, "r") as f:
        file_content_string = f.read(MAX_CHARS)

    return file_content_string
