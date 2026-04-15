# ex 1: break the loop when the condition is met
planets_list = ["mercury", "venus", "earth", "mars", "jupiter", "saturn", "uranus"]
for planet in planets_list:
    print(planet)
    if (planet == "mars"):
        break


# ex 2: break the loop but not inclusively
planets_list = ["mercury", "venus", "earth", "mars", "jupiter", "saturn", "uranus"]
for planet in planets_list:
    if planet == "jupiter":  # 1 step after
        break
    print(planet)