def counter(x):
    for i in range(1,x+1):
        yield i**2

x = int(input())
get_obj = counter(x)
for i in get_obj:
    print(i)