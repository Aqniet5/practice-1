def down(x):
    for i in range(x,-1,-1):
        yield i

x = int(input())
gen_obj = down(x)
for i in gen_obj:
    print(i)