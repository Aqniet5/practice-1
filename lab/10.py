class Car:
    def __init__(self,name,year):
        self.name = name
        self.year = year
        self.distance = 0
first_car = Car("Audi",2026)
print(first_car.distance)
first_car.distance = 100
print(first_car.distance)