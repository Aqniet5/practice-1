import re
#Akniyet_2008
pattern = re.compile(r"^[^A-Za-z0-9\_]{1,10}$")
word = '++++++++++'
if pattern.search(word):
    print("Done")
else:
    print("Not done")