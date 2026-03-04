f = open("demofile.txt")
print(f.read())

with open("demofile.txt") as ff:
  print(ff.read())