import re
text = input()
matches = re.findall(r"[a-z]+\_[a-z]+",text)
print(matches)
