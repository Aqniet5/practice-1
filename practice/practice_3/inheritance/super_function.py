class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        print(f"{self.name} makes a sound")

# Child class
class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)  # Call the parent __init__
        self.breed = breed

    def speak(self):
        super().speak()  # Call the parent speak()
        print(f"{self.name} barks")

# Create object
my_dog = Dog("Buddy", "Labrador")
my_dog.speak()
