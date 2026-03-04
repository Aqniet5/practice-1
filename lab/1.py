import re
pattern = re.compile(r"^[a-z]+$")
word = "hello"
if pattern.search(word):
    print('yes')
else:
    print('no')