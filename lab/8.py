# class Animals is declared
class Animals:
    
    # constructor
    def __init__(self):
        
        # keys are initialized with
        # their respective values
        self.lion = 'carnivore'
        self.dog = 'omnivore'
        self.giraffe = 'herbivore'

    def printit(self):
        print("Dictionary from the object fields\
        belonging to the class Animals:")


# object animal of class Animals
animal = Animals()

# calling printit method
animal.printit()
# calling attribute __dict__ on animal
# object and printing it
print(animal.__dict__)