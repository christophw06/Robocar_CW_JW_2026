import queue
import threading

import logic
import motor

motor.init()


def stop_all_wheels():
    motor.front_left(0)
    motor.front_right(0)
    motor.rear_left(0)
    motor.rear_right(0)


def drive_in_direction(speed_left, speed_right):
    while True:
        get_speed_input_left = speed_left.get()
        get_speed_input_right = speed_right.get()
        if (
            0 < abs(get_speed_input_left) <= 100
            and 0 <= abs(get_speed_input_right) <= 100
        ):
            right_wheel_speed = int(get_speed_input_right)
            left_wheel_speed = int(get_speed_input_left)

        motor.front_left(left_wheel_speed)
        motor.front_right(right_wheel_speed)
        motor.rear_left(left_wheel_speed)
        motor.rear_right(right_wheel_speed)


drive_test = threading.Thread(
    target=drive_in_direction, args=(logic.speed_left_wheel, logic.speed_right_wheel)
)

drive_test.start()
