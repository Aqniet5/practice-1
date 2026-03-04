import re
text = "thisIsCamelCaseString"
snake_case = re.sub(r'([A-Z])', r'_\1', text).lower()
print(snake_case)