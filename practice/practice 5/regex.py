#Regex solving problems

#1Task
import re
s = input()
print(bool(re.fullmatch(r"ab*", s)))

#2Task
import re
s = input()
print(bool(re.fullmatch(r"ab{2,3}", s)))

#3Task
import re
s = input()
print(re.findall(r"\b[a-z]+_[a-z]+\b", s))

#4Task
import re
s = input()
print(re.findall(r"\b[A-Z][a-z]+\b", s))

#5Task
import re
s = input()
print(bool(re.fullmatch(r"a.*b", s)))

#6Task
import re
s = input()
print(re.sub(r"[ ,\.]", ":", s))

#7Tassk
s = input().strip()
parts = s.split("_")
print(parts[0] + "".join(p.capitalize() for p in parts[1:]))

#8Task
import re
s = input()
print(re.split(r"(?=[A-Z])", s))

#9Task
import re
s = input()
print(re.sub(r"(?<!^)(?=[A-Z])", " ", s))

#10Task
import re
s = input().strip()
s = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", s)
s = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s)
print(s.lower())