class Reverse:
    def __init__(self,string):
        self.string = string
    def reversing(self):
        for i in reversed(self.string):
            print(i,end="")
            
s = input()
a = Reverse(s)
a.reversing()
