import math

class Circle:
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2


# Input
r = int(input())

# Create circle
c = Circle(r)

# Calculate and print area
area = c.area()
print(f"{area:.2f}")
