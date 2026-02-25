from datetime import datetime
import math

fmt = "%Y-%m-%d %H:%M:%S"

date1 = datetime.strptime(input(), fmt)
date2 = datetime.strptime(input(), fmt)

print(abs((date1 - date2).total_seconds()))