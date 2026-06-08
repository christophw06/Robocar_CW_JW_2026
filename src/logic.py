import queue
import threading

import motor
import pid

motor.init()
position_of_line = queue.Queue(maxsize=1)
speed_left_wheel = queue.Queue(maxsize=1)
speed_right_wheel = queue.Queue(maxsize=1)


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


def calculate_position():
    global position_of_line

    while True:
        position_value = (
            (-1 * pid.average_left) + (0 * pid.average_mid) + (1 * pid.average_right)
        )
        position_of_line.put(position_value)
        # -1 line is left, 0 line ist middle, 1 line is right


def set_speed_to_drive(base_speed, turn_faktor):
    global position_of_line, speed_right_wheel, speed_left_wheel
    while True:
        position = position_of_line.get()
        speed_left = base_speed + (position * turn_faktor)
        speed_right = base_speed - (position * turn_faktor)
        speed_left_wheel.put(speed_left)
        speed_right_wheel.put(speed_right)


direction_calculation = threading.Thread(target=calculate_position)
speed_setting = threading.Thread(target=set_speed_to_drive, args=(30, 30))
drive_test = threading.Thread(
    target=drive_in_direction, args=(speed_left_wheel, speed_right_wheel)
)

direction_calculation.start()
speed_setting.start()
drive_test.start()
pid.values_to_process_mid.start()
pid.calculate_average_mid.start()
pid.values_to_process_right.start()
pid.calculate_average_right.start()
pid.values_to_process_left.start()
pid.calculate_average_left.start()
