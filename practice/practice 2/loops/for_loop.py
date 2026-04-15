# ex 1: print values in a list by looping
fruits_list = ["apple", "banana", "mango", "orange", "grape", "peach", "kiwi"]
for fruit in fruits_list:
    print(fruit)

# ex 2: looping through a string
fruit = "Banana"
for letter in fruit:
    print(letter)  # class <'char'>

# ex 3: looping with a range
for x in range(6):
    print(x)

# ex 4: nested loops
a = [1, 2, 3]
b = [4, 5, 6]
for i in a:
    for j in b:
        print(f"({i, j})")

# ex 5: pass
fruits_list = ["apple", "banana", "mango", "orange", "grape", "peach", "kiwi"]
for fruit in fruits_list:
    pass