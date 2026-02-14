def add(a, b):
    return a + b

result = add(5, 3)
print(result)  # Output: 8


def get_name_age():
    name = "Alice"
    age = 25
    return name, age

person_name, person_age = get_name_age()
print(person_name)  # Output: Alice
print(person_age)   # Output: 25


def check_number(num):
    if num > 0:
        return "Positive"
    elif num < 0:
        return "Negative"
    else:
        return "Zero"

print(check_number(10))  # Output: Positive
print(check_number(-5))  # Output: Negative
print(check_number(0))   # Output: Zero
