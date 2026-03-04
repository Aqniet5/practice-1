from functools import reduce
numbers = [1, 2, 3, 4]

squared = map(lambda x: x**2, numbers)

print(list(squared))

evens = filter(lambda x: x % 2 == 0, numbers)

print(list(evens))



numbers = [1, 2, 3, 4]

total = reduce(lambda a, b: a + b, numbers)

print(total)