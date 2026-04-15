names = ["Alice", "Bob", "Charlie"]
scores = [90, 85, 78]

for i, (name, score) in enumerate(zip(names, scores), start=1):
    print(i, name, score)