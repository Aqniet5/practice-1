def isdivisible(x):
    for i in range(0,x+1):
        yield i
x = int(input())
gen_obj = isdivisible(x)
for i in gen_obj:
    if i % 3 == 0 and i % 4 == 0:
        print(i,end=" ")