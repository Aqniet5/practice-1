class Shape:
    def area(self):
        return 0
    
class Rectangular(Shape):
    def __init__(self,length,width):
        self.length = length
        self.width = width
    def area(self):
        return self.length * self.width
x,y = map(int,input().split())
p = Rectangular(x,y)
print(p.area())