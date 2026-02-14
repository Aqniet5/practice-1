numbers = [1, 2, 3, 4, 5, 6]

even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print(even_numbers)  # Output: [2, 4, 6]


numbers = [1, 2, 3, 4, 5, 6]

greater_than_3 = list(filter(lambda x: x > 3, numbers))
print(greater_than_3)  # Output: [4, 5, 6]
