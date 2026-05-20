import motor
import time

motor.init()

def stop_all_wheels():
    motor.front_left(0)
    motor.front_right(0)
    motor.rear_left(0)
    motor.rear_right(0)


time.sleep(3)
stop_all_wheels()
