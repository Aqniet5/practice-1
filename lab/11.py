class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade
    def __repr__(self):
        return f"Student({self.name!r}, {self.grade})"

students = [
    Student('Alice', 85),
    Student('Bob', 92),
    Student('Charlie', 85),
    Student('David', 90),
]
students.sort(key=lambda x:(-x.grade,x.name))
print(students)