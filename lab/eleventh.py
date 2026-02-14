class Pair:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def add(self, other):
        return Pair(self.a + other.a, self.b + other.b)


# Input
a1, b1, a2, b2 = map(int, input().split())

# Create Pair objects
p1 = Pair(a1, b1)
p2 = Pair(a2, b2)

# Add pairs
result = p1.add(p2)

# Output
print(f"Result: {result.a} {result.b}")
