import sys
n = int(input("How many elements?: "))
m = set()
for i in range(0,n):
    x = int(input(f"{i} element"))
    m.add(x)
print(sys.getsizeof(m))