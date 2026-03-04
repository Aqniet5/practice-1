import re
text = "this_is_snake_case"
components = text.split('_')
camel_case = components[0] + ''.join(x.title() for x in components[1:])
print(camel_case)