import os

os.mkdir("my_folder")

folders = ["data", "logs", "output"]
for folder in folders:
    os.mkdir(folder)