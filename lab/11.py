number, l, r = map(int, input().split())
arr = list(map(int, input().split()))

# Convert l and r to 0-based
l -= 1
r -= 1

# Reverse the subarray
arr[l:r+1] = arr[l:r+1][::-1]

print(*arr)
