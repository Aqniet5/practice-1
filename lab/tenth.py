class Person:
    def __init__(self, name):
        self.name = name


class Student(Person):
    def __init__(self, name, gpa):
        super().__init__(name)   # Call parent constructor
        self.gpa = gpa

    def display(self):
        print(f"Student: {self.name}, GPA: {self.gpa}")


# Input
name, gpa = input().split()
gpa = float(gpa)

# Create student object
student = Student(name, gpa)

# Output
student.display()
