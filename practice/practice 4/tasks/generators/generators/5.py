def decreasing(n):
    for i in range(n,-1,-1):
        yield i
n = int(input())
for e in decreasing(n):
    print(e)