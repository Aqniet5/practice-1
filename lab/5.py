n = int(input())

if n < 1:
    print("NO")
else:
    while n > 1:
        if n % 2 != 0:
            print("NO")
            break
        n = n // 2
    else:
        
        print("YES")
