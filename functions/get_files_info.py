import os


def get_files_info(working_directory, directory="."):
    target_path = os.path.abspath(os.path.join(working_directory, directory))
    working_path = os.path.abspath(working_directory)

    if not target_path.startswith(working_path):
        return f'\tError: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(target_path):
        return f'\tError: "{directory}" is not a directory'

    output_string = ""
    for item in os.listdir(target_path):
        abs_item_path = os.path.abspath(os.path.join(target_path, item))
        output_string += f" - {item}: file_size={os.path.getsize(abs_item_path)}, is_dir={os.path.isdir(abs_item_path)}\n"

    return output_string
