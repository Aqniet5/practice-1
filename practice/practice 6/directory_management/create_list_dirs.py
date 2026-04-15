import os


def list_directories(path):
    try:
        items = os.listdir(path)
    except FileNotFoundError:
        print(f"Path not found: {path}")
        return
    except PermissionError:
        print(f"Permission denied: {path}")
        return

    directories = []

    for item in items:
        full_path = os.path.join(path, item)
        if os.path.isdir(full_path):
            directories.append(item)

    if not directories:
        print("No directories found.")
    else:
        print("Directories:")
        for d in directories:
            print("-", d)


# Case 1: current directory
list_directories(".")

print()

# Case 2: specified directory
list_directories(r"C:\Users\User\Desktop\Semester 2\pp2_spring")