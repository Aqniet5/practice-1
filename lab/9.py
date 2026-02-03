n = int(input())
arr = list(map(int, input().split()))

maximum = max(arr)
minimum = min(arr)

for i in range(n):
    if arr[i] == maximum:
        arr[i] = minimum

print(*arr)#space separated output
