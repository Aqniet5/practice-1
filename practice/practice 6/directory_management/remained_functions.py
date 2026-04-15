import os
import shutil


def recreate_folder(folder_name):
    # Remove folder if it exists, then create a fresh one
    if os.path.exists(folder_name):
        shutil.rmtree(folder_name)

    os.mkdir(folder_name)
    print(f"{folder_name} has been created.")


def create_nested_dirs(path):
    os.makedirs(path, exist_ok=True)
    print(f"Nested path ensured: {path}")


def change_and_show_dir(path):
    try:
        os.chdir(path)
        print("Current directory:", os.getcwd())
    except FileNotFoundError:
        print("Directory not found:", path)


def create_file_once(folder, filename, content):
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, filename)

    try:
        with open(file_path, "x", encoding="utf-8") as f:
            f.write(content)
        print("File created:", file_path)
    except FileExistsError:
        print("File already exists:", file_path)


# --- Usage ---

# ex 1
recreate_folder("folder1")

# ex 2
create_nested_dirs("folder1/folder2/folder3")

# ex 3
change_and_show_dir("..")

# ex 4 (file creation)
create_file_once(
    "builtin_functions",
    "map_filter_reduce.py",
    "n = int(input())  # example content"
)