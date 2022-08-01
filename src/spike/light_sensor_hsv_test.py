# ここにコードを書いてね :-)
import hub
import time
import re
from avoid_color_sign import Avoid_color_sign
from gyro import Gyro
from basic_motion import Basic_motion
print("--devce init--")

while True:
    motor = hub.port.C.motor
    motor_steer = hub.port.E.motor
    ser = hub.port.D
    light_sensor = hub.port.A.device
    port_a = hub.port.A
    if ser == None or motor == None or motor_steer == None or light_sensor == None or port_a == None:
        print("Please check port!!")
        time.sleep(1)
        continue
    hub.motion.yaw_pitch_roll(0)
    motor.mode(2)
    ser.mode(hub.port.MODE_FULL_DUPLEX)
    motor_steer.mode(2)
    light_sensor.mode(6)
    time.sleep(2)
    ser.baud(115200)
    time.sleep(1)
    break
while True:
    time.sleep(1)
    h = light_sensor.get(2)[0]
    s = light_sensor.get(2)[1]

    v = light_sensor.get(2)[2]

    print("h,s,v:",h,s,v)
