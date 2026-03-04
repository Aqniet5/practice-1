import re
text = input()
matches = re.findall(r"[A-Z][a-z]+",text)
print(matches)