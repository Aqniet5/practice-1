class Animal:
    def speak(self):
        print("Animal makes a sound")

class Dog(Animal):
    def speak(self):
        print("Dog barks")  # This overrides Animal's speak()

# Create objects
animal = Animal()
dog = Dog()

animal.speak()  # Output: Animal makes a sound
dog.speak()     # Output: Dog barks
