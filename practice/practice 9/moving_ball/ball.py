class Ball:
    def __init__(self, x, y, step, radius, width, height):
        self.x = x
        self.y = y
        self.step = step
        self.radius = radius
        self.width = width
        self.height = height

    def move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy

        if self.radius <= new_x <= self.width - self.radius:
            self.x = new_x

        if self.radius <= new_y <= self.height - self.radius:
            self.y = new_y