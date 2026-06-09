import queue
import threading
import time

from gpiozero import LineSensor

linesensor_right = LineSensor(23)
linesensor_mid = LineSensor(15)
linesensor_left = LineSensor(14)

sensor_values_mid = queue.Queue()
sensor_values_right = queue.Queue()
sensor_values_left = queue.Queue()


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


def get_value_sensor_in_list_mid(
    sensor_function,
    readin_timestep_in_ms,
    number_of_values_to_readin,
):
    global sensor_values_mid

    while True:
        sensor_value_of_func = sensor_function("mid")
        number_of_values = sensor_values_mid.qsize()
        if sensor_value_of_func:
            sensor_value_converted = 1
        else:
            sensor_value_converted = 0

        if number_of_values < number_of_values_to_readin:
            sensor_values_mid.put(sensor_value_converted)
            time.sleep((readin_timestep_in_ms / number_of_values_to_readin) / 100)
        elif number_of_values >= number_of_values_to_readin:
            sensor_values_mid.get()
            sensor_values_mid.put(sensor_value_converted)
            time.sleep((readin_timestep_in_ms / number_of_values_to_readin) / 100)


"""def get_value_sensor_in_list_right(
    sensor_function,
    readin_timestep_in_ms,
    number_of_values_to_readin,
):
    global sensor_values_right

    while True:
        sensor_value_of_func = sensor_function("right")
        number_of_values = sensor_values_right.qsize()
        if sensor_value_of_func:
            sensor_value_converted = 1
        else:
            sensor_value_converted = 0

        if number_of_values < number_of_values_to_readin:
            sensor_values_right.put(sensor_value_converted)
            time.sleep((readin_timestep_in_ms / number_of_values_to_readin) / 100)
        elif number_of_values >= number_of_values_to_readin:
            sensor_values_right.get()
            sensor_values_right.put(sensor_value_converted)
            time.sleep((readin_timestep_in_ms / number_of_values_to_readin) / 100)"""


def get_value_sensor_in_list_left(
    sensor_function,
    readin_timestep_in_ms,
    number_of_values_to_readin,
):
    global sensor_values_left

    while True:
        sensor_value_of_func = sensor_function("left")
        number_of_values = sensor_values_left.qsize()
        if sensor_value_of_func:
            sensor_value_converted = 1
        else:
            sensor_value_converted = 0

        if number_of_values < number_of_values_to_readin:
            sensor_values_left.put(sensor_value_converted)
            time.sleep((readin_timestep_in_ms / number_of_values_to_readin) / 100)
        elif number_of_values >= number_of_values_to_readin:
            sensor_values_left.get()
            sensor_values_left.put(sensor_value_converted)
            time.sleep((readin_timestep_in_ms / number_of_values_to_readin) / 100)

            time.sleep((readin_timestep_in_ms / number_of_values_to_readin) / 100)


values_to_process_mid = threading.Thread(
    target=get_value_sensor_in_list_mid,
    args=(sensor_line, 10, 5),
)

"""values_to_process_right = threading.Thread(
    target=get_value_sensor_in_list_right,
    args=(sensor_line, 10, 5),
)"""

values_to_process_left = threading.Thread(
    target=get_value_sensor_in_list_left,
    args=(sensor_line, 10, 5),
)

values_to_process_mid.start()

"""values_to_process_right.start()"""

values_to_process_left.start()
