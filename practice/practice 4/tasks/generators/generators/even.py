def evens(n):
    for i in range(0,n+1):
        if i % 2 == 0:
            yield i

n = int(input())
for even in evens(n):
    if even == n:
        print(even)
    else:
        print(even,end=",")