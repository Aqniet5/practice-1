def generator(a,b):
    for i in range(a,b+1):
        yield i**2
x,y = list(map(int,input().split()))
gen_obj = generator(x,y)
for i in gen_obj:
    print(i)