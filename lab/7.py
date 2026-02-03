n = int(input())
arr = list(map(int, input().split()))

maximum = arr[0]
position = 0

for i in range(1, n):
    if arr[i] > maximum:
        maximum = arr[i]
        position = i

print(position + 1)
