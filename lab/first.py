def valid(number):
    itis = True
    for i in number:
        if(int(i) % 2 != 0):
            itis = False
            break
    if(itis):
        print("Valid")
    else:
        print("Not valid")
x = input()
valid(x)