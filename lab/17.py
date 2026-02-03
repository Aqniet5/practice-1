n = int(input())

freq = {}

for i in range(n):
    number = input()
    if number in freq:
        freq[number] += 1
    else:
        freq[number] = 1

answer = 0
for number in freq:
    if freq[number] == 3:
        answer += 1

print(answer)
