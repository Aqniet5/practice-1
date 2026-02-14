class Dog:
    species = "Canis familiaris"  # Class variable

    def __init__(self, name, age):
        self.name = name  # Instance variable
        self.age = age    # Instance variable

# Create objects
dog1 = Dog("Buddy", 3)
dog2 = Dog("Lucy", 5)

print(dog1.name)      # Output: Buddy (instance variable)
print(dog2.name)      # Output: Lucy  (instance variable)

print(dog1.species)   # Output: Canis familiaris (class variable)
print(dog2.species)   # Output: Canis familiaris (class variable)
