nums = [1, 2, 3, 4, 5, 6]

evens = list(filter(lambda x: x % 2 == 0, nums))

print(evens)

from functools import reduce

nums2 = [1, 2, 3, 4]

result = reduce(lambda x, y: x + y, nums2)

print(result)