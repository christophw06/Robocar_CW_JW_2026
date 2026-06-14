import time

import sensor

last_pos_for_pid = 0.0
integral = 0.0


# readin of sensor values and calculating speed for left and right side
def pid_speed_calculation(refreshrate_in_Hz, base_speed, kp, ki, kd, ks):
    global last_pos_for_pid, integral

    integral_reset = 0
    sleep_time_refreshrate = 1 / refreshrate_in_Hz

    sensor_value_right = sensor.pos_sensor_over_line("right")
    sensor_value_left = sensor.pos_sensor_over_line("left")
    sensor_value_mid = sensor.pos_sensor_over_line("mid")

    position = sensor.interpret_position(
        sensor_value_left, sensor_value_mid, sensor_value_right
    )

    # previous position is used if no sensor reads back values
    if position is None:
        position = last_pos_for_pid
        integral = integral_reset

    # declare P, I and D for calculation
    proportional = position
    integral = integral + position
    derivativ = last_pos_for_pid - position

    limited_integral = max(-20, min(20, integral))
    integral = limited_integral

    # calculate correction factor with PID
    correction_factor = kp * proportional + ki * limited_integral + kd * derivativ

    # set speed values for left and right side
    dynamic_base_speed = base_speed - (abs(position) * ks)
    speed_left = dynamic_base_speed + correction_factor
    speed_right = dynamic_base_speed - correction_factor

    # store last position for derivativ next call
    last_pos_for_pid = position

    time.sleep(sleep_time_refreshrate)

    return speed_left, speed_right
