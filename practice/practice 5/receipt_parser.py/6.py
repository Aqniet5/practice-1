import re
text = "Hello, world. How are you?"
new_text = re.sub(r"[ ,\.]", ":", text)
print(new_text)