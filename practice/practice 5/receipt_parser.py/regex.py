import re
txt = "The rain in Spain"
x = re.search("^The.*Spain$", txt)
y = re.findall("ai", txt)
print(y)
z = re.search("\s", txt)

print("The first white-space character is located in position:", z.start())