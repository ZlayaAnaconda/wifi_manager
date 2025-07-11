import math
from time import sleep
from config import *
from services.bdWrapper import *


def get_price(area,wifi):
    step = int(get_setting(12))
    cost = int(get_setting(13))
    steps_amount = math.ceil(int(area) / step)
    if wifi == "Да" or wifi == "да":
        return steps_amount * cost + 15
    else:
        return steps_amount * cost