# ex 1: inheriting parameters from parent class
class Person():
    def __init__(self, name):
        self.name = name

class Student(Person):
    def __init__(self, name):
        super().__init__(name) # inherits from parent class

# ex 2: add property

class Person_2():
    def __init__(self, name, sname):
        self.name = name
        self.sname = sname

class Student_2(Person_2):
    def __init__(self, name, sname):
        super().__init__(name, sname)
    graduation_date = 2019 # class variable
