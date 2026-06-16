import json
import os

import logic
import motor


def get_values_of_json(needed_value):
    json_file = "config.json"
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path_json_file = os.path.join(base_dir, json_file)
    with open(path_json_file, "r") as config_file:
        config_data = json.load(config_file)
    return config_data[str(needed_value)]


def stop_all_wheels():
    MOTOR_SPEED_STOP = 0
    motor.front_left(MOTOR_SPEED_STOP)
    motor.front_right(MOTOR_SPEED_STOP)
    motor.rear_left(MOTOR_SPEED_STOP)
    motor.rear_right(MOTOR_SPEED_STOP)


def reduce_turn_radius(speed_left, speed_right, turn_factor):
    if speed_left < 0:
        rear_wheel_left = speed_left * turn_factor
        rear_wheel_right = speed_right
        return rear_wheel_left, rear_wheel_right
    elif speed_right < 0:
        rear_wheel_left = speed_left
        rear_wheel_right = speed_right * turn_factor
        return rear_wheel_left, rear_wheel_right
    else:
        return speed_left, speed_right


# initialize motors, loops through the PID and set motor speed
def start_driving():
    motor.init()
    LIMITER_MAX = 100
    LIMITER_MIN = -100
    refreshrate = get_values_of_json("refreshrate in Hz")
    base_speed = get_values_of_json("base speed")
    kp = get_values_of_json("proportional factor")
    ki = get_values_of_json("integral factor")
    kd = get_values_of_json("derivativ factor")
    ks = get_values_of_json("dynamicspeed factor")
    turn_factor = get_values_of_json("turn factor")

    while True:
        left_side_speed, right_side_speed = logic.pid_speed_calculation(
            refreshrate, base_speed, kp, ki, kd, ks
        )

        rear_left_speed, rear_right_speed = reduce_turn_radius(
            left_side_speed, right_side_speed, turn_factor
        )

        left_side_speed_limited = max(LIMITER_MIN, min(LIMITER_MAX, left_side_speed))
        right_side_speed_limited = max(LIMITER_MIN, min(LIMITER_MAX, right_side_speed))
        left_rear_speed_limited = max(LIMITER_MIN, min(LIMITER_MAX, rear_left_speed))
        right_rear_speed_limited = max(LIMITER_MIN, min(LIMITER_MAX, rear_right_speed))

        motor.front_left(left_side_speed_limited)
        motor.front_right(right_side_speed_limited)
        motor.rear_left(left_rear_speed_limited)
        motor.rear_right(right_rear_speed_limited)


try:
    start_driving()
except KeyboardInterrupt:
    stop_all_wheels()
