import copy
lists = [i**2 for i in range(1,11) if i % 2==0]
for i in lists:
    print(i,end=" ")

list1 = lists[:]
list1.append(5)
for i in lists:
    print(i,end=" ")