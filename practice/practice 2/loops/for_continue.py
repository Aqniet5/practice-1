# ex 1: skip a value, or continue usage
colors_list = ["red", "blue", "green", "yellow", "black", "white", "purple"]
for color in colors_list:
    if color == "black":
        continue
    print(color)
# ex 2: skip a value to avoid errors:
division_values = [-3, -2, -1, 0, 1, 2, 3]
for i in division_values:
    if i == 0:
        continue
    print(10 / i)