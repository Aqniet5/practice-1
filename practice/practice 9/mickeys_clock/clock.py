import math
from datetime import datetime


def get_time_angles():
    now = datetime.now()

    seconds = now.second
    minutes = now.minute

    sec_angle = (seconds * 6) - 90
    min_angle = (minutes * 6) - 90

    return sec_angle, min_angle