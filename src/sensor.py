import time

from gpiozero import LineSensor

linesensor_right = LineSensor(23)
linesensor_mid = LineSensor(15)
linesensor_left = LineSensor(14)


def sensor_line(sensor_orientation):
    if sensor_orientation == "right":
        while linesensor_right.value == 1:
            return True
        else:
            return False
    elif sensor_orientation == "left":
        while linesensor_left.value == 1:
            return True
        else:
            return False
    else:
        while linesensor_mid.value == 1:
            return True
        else:
            return False
