n = int(input())

episodes = {}  

for i in range(n):
    s, k = input().split()
    k = int(k)

    if s in episodes:
        episodes[s] += k
    else:
        episodes[s] = k


names = list(episodes.keys())
names.sort()


for name in names:
    print(name, episodes[name])
