import re 
text = input()
matches = re.findall(r"a.*b",text)
print(matches)