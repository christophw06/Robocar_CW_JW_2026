import queue
import threading
import time

import sensor

sensor_values = queue.Queue()


def get_value_sensor_in_list(
    sensor_function,
    sensor_orientation,
    readin_timestep_in_ms,
    number_of_values_to_readin,
):
    global sensor_values
    while True:
        sensor_value_of_func = sensor_function(sensor_orientation)
        number_of_values = sensor_values.qsize()
        if sensor_value_of_func:
            sensor_value_converted = 1
        else:
            sensor_value_converted = 0

        if number_of_values < number_of_values_to_readin:
            sensor_values.put(sensor_value_converted)
            time.sleep((readin_timestep_in_ms / number_of_values_to_readin) / 100)
        elif number_of_values >= number_of_values_to_readin:
            sensor_values.get()
            sensor_values.put(sensor_value_converted)
            time.sleep((readin_timestep_in_ms / number_of_values_to_readin) / 100)

        print(list(sensor_values.queue))


"!!!average calculating extend and correct with queue -> threading with both functions and one list possible"


def average_value(values_list):
    while True:
        number_to_divide = len(values_list)
        if number_to_divide > 0:
            average_value = sum(values_list) / number_to_divide
            print(average_value)
            return average_value


values_to_process = threading.Thread(
    target=get_value_sensor_in_list,
    args=(sensor.sensor_line, "mid", 200, 10),
)

# calculate_average = threading.Thread(target=average_value, args=sensor_values)

values_to_process.start()
# calculate_average.start()
