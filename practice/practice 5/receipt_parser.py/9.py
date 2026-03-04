import re
text = "ThisIsATestString"
spaced = re.sub(r"([A-Z])", r" \1", text).strip()
print(spaced)