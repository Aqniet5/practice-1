numberx = int(input())
isit = True
i = 2  

while i * i <= numberx:  
    if numberx % i == 0:
        isit = False
        break
    i += 1

if numberx < 2:
    isit = False

if isit:
    print("YES")
else:
    print("NO")