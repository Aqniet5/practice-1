class Myclass:
    def __init__(self):
        self.elephant = "Calf"
        self.shark = "Sharky"
a = Myclass()
for key,value in a.__dict__.items():
    print(key,value)