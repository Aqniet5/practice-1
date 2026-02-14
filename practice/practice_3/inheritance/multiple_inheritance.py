class Father:
    def skills(self):
        print("Gardening, Programming")

class Mother:
    def skills(self):
        print("Cooking, Art")

# Child inherits from both Father and Mother
class Child(Father, Mother):
    pass

c = Child()
c.skills()
