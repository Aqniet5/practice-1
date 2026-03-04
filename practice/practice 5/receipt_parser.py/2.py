import re
text = "a abb abb ab bbbb abbbb"
matches = re.findall(r"ab{2,3}",text)
print(matches)