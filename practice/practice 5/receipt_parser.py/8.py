import re
text = "CamelCaseStringExample"
parts = re.split(r"(?=[A-Z])", text)
print(parts)