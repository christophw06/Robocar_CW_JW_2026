import queue
import threading

import sensor

position_of_line = queue.Queue(maxsize=1)
speed_left_wheel = queue.Queue(maxsize=1)
speed_right_wheel = queue.Queue(maxsize=1)


last_position_for_pid = 0.0
average_mid = 0
average_right = 0
average_left = 0


def calc_average_value(values_list, orientation):
    while True:
        number_to_divide = values_list.qsize()
        if orientation == "right" and number_to_divide > 0:
            global average_right
            average_right = round(sum(list(values_list.queue)) / number_to_divide, 1)
        elif orientation == "left" and number_to_divide > 0:
            global average_left
            average_left = round(sum(list(values_list.queue)) / number_to_divide, 1)
        elif orientation == "mid" and number_to_divide > 0:
            global average_mid
            average_mid = round(sum(list(values_list.queue)) / number_to_divide, 1)


def calculate_position():
    global position_of_line, average_left, average_mid

    while True:
        position_value = (-1 * average_left) + (1 * average_mid)
        position_of_line.put(position_value)
        # -1 line is left, 0 line ist middle, 1 line is right


def pid_drive(base_speed, kp, ki, kd):
    global position_of_line, speed_right_wheel, speed_left_wheel, last_position_for_pid
    difference_summe_for_i = 0.0
    while True:
        position = position_of_line.get()
        difference_summe_for_i += position
        correction_factor = (
            (position * kp)
            + (difference_summe_for_i * ki)
            + (kd * (position - last_position_for_pid))
        )
        last_position_for_pid = position
        speed_left = base_speed + correction_factor
        speed_right = base_speed - correction_factor
        speed_right_wheel.put(speed_right)
        speed_left_wheel.put(speed_left)


direction_calculation = threading.Thread(target=calculate_position)
speed_setting = threading.Thread(target=pid_drive, args=(10, 30, 0.5, 5))
calculate_average_mid = threading.Thread(
    target=calc_average_value, args=(sensor.sensor_values_mid, "mid")
)

"""calculate_average_right = threading.Thread(
    target=calc_average_value, args=(sensor.sensor_values_right, "right")
)"""

calculate_average_left = threading.Thread(
    target=calc_average_value, args=(sensor.sensor_values_left, "left")
)

direction_calculation.start()
speed_setting.start()
calculate_average_mid.start()
"""calculate_average_right.start()"""
calculate_average_left.start()
