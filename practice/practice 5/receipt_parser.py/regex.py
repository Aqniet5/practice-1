import re
text = "a aab aabb abb abbbb"
matches = re.findall(r"ab*",text)
print(matches)