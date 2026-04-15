
# =========================
# 1. Numeric Types
# =========================

integer_num = 10
float_num = 3.14
complex_num = 2 + 3j

print("=== Numeric Types ===")
print("Integer:", integer_num, type(integer_num))
print("Float:", float_num, type(float_num))
print("Complex:", complex_num, type(complex_num))


# =========================
# 2. String Type
# =========================

text = "Hello Python"
single_char = 'A'

print("\n=== String Type ===")
print("Text:", text, type(text))
print("Character:", single_char, type(single_char))


# =========================
# 3. Boolean Type
# =========================

is_active = True
is_logged_in = False

print("\n=== Boolean Type ===")
print("is_active:", is_active, type(is_active))
print("is_logged_in:", is_logged_in, type(is_logged_in))


# =========================
# 4. List Type (mutable)
# =========================

fruits = ["apple", "banana", "cherry"]

print("\n=== List Type ===")
print("Fruits:", fruits, type(fruits))

fruits.append("orange")
print("After append:", fruits)


# =========================
# 5. Tuple Type (immutable)
# =========================

colors = ("red", "green", "blue")

print("\n=== Tuple Type ===")
print("Colors:", colors, type(colors))


# =========================
# 6. Set Type (unique values)
# =========================

numbers = {1, 2, 2, 3, 4, 4, 5}

print("\n=== Set Type ===")
print("Set:", numbers, type(numbers))


# =========================
# 7. Dictionary Type (key-value)
# =========================

student = {
    "name": "Akniyet",
    "age": 16,
    "grade": "A"
}

print("\n=== Dictionary Type ===")
print("Student:", student, type(student))

print("Name:", student["name"])


# =========================
# 8. Type conversion examples
# =========================

print("\n=== Type Conversion ===")

num_str = "100"
num_int = int(num_str)
num_float = float(num_str)

print("String:", num_str, type(num_str))
print("To int:", num_int, type(num_int))
print("To float:", num_float, type(num_float))


# =========================
# 9. Checking type dynamically
# =========================

value = [1, 2, 3]

print("\n=== Type Checking ===")
if isinstance(value, list):
    print("This is a list")
else:
    print("Not a list")