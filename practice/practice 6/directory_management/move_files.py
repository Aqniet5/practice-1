import os
import shutil


def move_and_read_file(source_path, destination_dir):
    # Validate source file
    if not os.path.isfile(source_path):
        print("Source file does not exist.")
        return

    # Ensure destination exists
    os.makedirs(destination_dir, exist_ok=True)

    # Move file
    file_name = os.path.basename(source_path)
    new_path = os.path.join(destination_dir, file_name)

    try:
        shutil.move(source_path, new_path)
        print(f"File moved to: {new_path}")
    except Exception as e:
        print(f"Move failed: {e}")
        return

    # Read file after moving
    try:
        with open(new_path, "r", encoding="utf-8") as file:
            content = file.read()
            print("File content:")
            print(content)
    except FileNotFoundError:
        print("File not found after moving.")
    except Exception as e:
        print(f"Read error: {e}")


# Example usage
source = "/Users/alim/Practises/practice/practice6/directory_management/file2.txt"
destination = os.getcwd()

move_and_read_file(source, destination)