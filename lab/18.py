n = int(input())

first_index = {}

for i in range(1, n + 1):
    s = input()
    if s not in first_index:
        first_index[s] = i
        
for s in sorted(first_index):
    print(s, first_index[s])