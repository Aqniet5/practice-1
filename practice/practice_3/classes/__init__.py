class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age

p1 = Person("Emil", 36)

print(p1.name)
print(p1.age)

class Person2:
  pass

p2 = Person2()
p2.name = "Tobias"
p2.age = 25

print(p2.name)
print(p2.age)