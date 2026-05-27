import motor
import time
import sensor

motor.init()

def stop_all_wheels():
    motor.front_left(0)
    motor.front_right(0)
    motor.rear_left(0)
    motor.rear_right(0)

def turn_right(turn_speed_right, turn_speed_left):
    right_wheel_speed=0
    left_wheel_speed=0

    if turn_speed_right > turn_speed_left and 0<= abs(turn_speed_left) <=100 and 0< abs(turn_speed_right) <=100:
        right_wheel_speed= int(turn_speed_right)
        left_wheel_speed= int(turn_speed_left)

    motor.front_left(left_wheel_speed)
    motor.front_right(right_wheel_speed)
    motor.rear_left(left_wheel_speed)
    motor.rear_right(right_wheel_speed)

def turn_left(turn_speed_left, turn_speed_right):
    right_wheel_speed= 0
    left_wheel_speed= 0
    if turn_speed_left > turn_speed_right and 0< abs(turn_speed_left) <=100 and 0<= abs(turn_speed_right) <=100:
        right_wheel_speed= int(turn_speed_right)
        left_wheel_speed=  int(turn_speed_left)

    motor.front_left(left_wheel_speed)
    motor.front_right(right_wheel_speed)
    motor.rear_left(left_wheel_speed)
    motor.rear_right(right_wheel_speed)

def drive_straight(drive_speed, direction):
    drive_speed_direction=0
    if direction == "f":
        drive_speed_direction = abs(drive_speed)
    elif direction == "r":
        drive_speed_direction = (-1)*abs(drive_speed)
    else:
        drive_speed_direction = 0

    motor.front_left(drive_speed_direction)
    motor.front_right(drive_speed_direction)
    motor.rear_left(drive_speed_direction)
    motor.rear_right(drive_speed_direction)

def line_detection_start_driving():
    while True:
        if sensor.sensor_line("left") == False and sensor.sensor_line("right") == False and sensor.sensor_line("mid"):
            drive_straight(20, "f")
        elif sensor.sensor_line("left") == False and sensor.sensor_line("right") and sensor.sensor_line("mid") == False:
            turn_left(20, 0)
        elif sensor.sensor_line("left") and sensor.sensor_line("right") == False and sensor.sensor_line("mid") == False:
            turn_right(20, 0)
        elif sensor.sensor_line("left") and sensor.sensor_line("right") and sensor.sensor_line("mid"):
            stop_all_wheels()

line_detection_start_driving()
