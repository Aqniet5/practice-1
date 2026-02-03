number = int(input())
arr = list(map(int,input().split()))
for i in range(0,number):
    print(arr[i]*arr[i],end=" ")