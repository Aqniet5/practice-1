import shutil
import os
with open("demofile.txt","r") as f:
    f.read()
with open("demofile.txt","a") as f:
    f.write("\n")
shutil.copy("demofile.txt","demofile2.py")

os.remove("demofile.txt")
os.remove('demofile2.py')