import datetime
x = datetime.datetime.now()
without_microsecond = x.replace(microsecond=0)
print(without_microsecond)