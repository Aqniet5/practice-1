# =========================
# 1. Variables and types
# =========================

name = "Akniyet"
age = 16
height = 1.75
is_student = True

print("Name:", name)
print("Age:", age)
print("Height:", height)
print("Is student:", is_student)

print("\n--- Types ---")
print(type(name))
print(type(age))
print(type(height))
print(type(is_student))


# =========================
# 2. Multiple assignment
# =========================

x, y, z = 10, 20, 30
print("\nMultiple assignment:", x, y, z)


# =========================
# 3. Same value assignment
# =========================

a = b = c = 100
print("Same value:", a, b, c)


# =========================
# 4. Type conversion
# =========================

num_str = "50"
num_int = int(num_str)
num_float = float(num_str)

print("\nType conversion:")
print(num_str, type(num_str))
print(num_int, type(num_int))
print(num_float, type(num_float))


# =========================
# 5. Basic operations with variables
# =========================

a = 15
b = 4

print("\nOperations:")
print("Addition:", a + b)
print("Subtraction:", a - b)
print("Multiplication:", a * b)
print("Division:", a / b)
print("Floor division:", a // b)
print("Modulus:", a % b)
print("Power:", a ** b)


# =========================
# 6. String variables
# =========================

first_name = "Ali"
last_name = "Khan"
full_name = first_name + " " + last_name

print("\nFull name:", full_name)

# f-string formatting
print(f"Hello, my name is {full_name} and I am {age} years old")


# =========================
# 7. User input variables
# =========================

# Uncomment to test interactively
# user_name = input("\nEnter your name: ")
# user_age = int(input("Enter your age: "))
# print(f"Welcome {user_name}, next year you will be {user_age + 1}")


# =========================
# 8. Swapping variables
# =========================

x, y = 5, 10
print("\nBefore swap:", x, y)

x, y = y, x
print("After swap:", x, y)