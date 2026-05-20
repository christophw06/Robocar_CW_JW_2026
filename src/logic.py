import motor
import time

def stop_all_wheels():
    motor.init()
    motor.front_left(0)
    motor.front_right(0)
    motor.rear_left(0)
    motor.rear_right(0)

def wheel_front_left():
    motor.init()
    motor.front_left(70)

wheel_front_left()
time.sleep(3)
stop_all_wheels()
