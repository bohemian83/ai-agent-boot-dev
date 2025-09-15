from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file


def tests(working_dir, directory):
    dir = directory
    if directory == ".":
        dir = "current"

    output = f"Results for '{dir}' directory:\n"
    output += get_files_info(working_dir, directory)

    return output


# print(tests("calculator", "."))
# print(tests("calculator", "pkg"))
# print(tests("calculator", "/bin"))
# print(tests("calculator", "../"))

# print(get_file_content("calculator", "main.py"))
# print(get_file_content("calculator", "pkg/calculator.py"))
# print(get_file_content("calculator", "/bin/cat"))
# print(get_file_content("calculator", "pkg/does_not_exist.py"))

print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))
