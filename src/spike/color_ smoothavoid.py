# ここにコードを書いてね :-)
import hub
import time
import re
from avoid_color_sign import Avoid_color_sign
from gyro import Gyro
print("--devce init--")

while True:
    motor = hub.port.A.motor
    motor_steer = hub.port.E.motor
    ser = hub.port.D
    light_sensor = hub.port.C.device
    if ser == None or motor == None or motor_steer == None or light_sensor == None:
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

avoid_color_sign = Avoid_color_sign(motor_steer,motor)
gyro = Gyro(motor_steer,motor,light_sensor)

def resetSerialBuffer():
    while True:
        reply = ser.read(10000)
        #print(reply)
        if reply == b"":
            break



if __name__ == "__main__":
    time.sleep(1)
    start = time.ticks_us()

    while True:
        reply = ser.read(10000)
        print(reply)
        if reply == b"":
            break

    end = time.ticks_us()
    print("elapse_time: {}[ms]".format((end-start)/1000))
    print("--waiting RasPi--")
    end_flag = False
    prev_steer = 0
    throttle = 0
    steer = 0
    count = 0
    red_flag = False
    green_flag = False
    blueline_flag = False
    orangeline_flag = False

    while True:
        cmd = ""
        red_flag = False
        green_flag = False
        blueline_flag = False
        orangeline_flag = False
        while True:
            red_flag = False
            green_flag = False
            blueline_flag = False
            orangeline_flag = False

            reply = ser.read(4 - len(cmd))
            reply = reply.decode("utf-8")
            cmd = cmd + reply
            #send distance
            '''distance = dist_sensor.get(2)[0]
            time.sleep(1/1000)
            #print("Distance: {}[cm]".format(distance))
            #time.sleep(1)
            if distance:
                ser.write("{:3d}@".format(distance))
            else:
                ser.write("{:3d}@".format(0))'''
            if len(cmd) >= 4 and cmd[-1:] == "@":
                cmd_list = cmd.split("@")
                if len(cmd_list) != 2:
                    print(len(cmd_list))
                    cmd = ""
                    continue

                #"end"を受け取ったとき、終了する
                if cmd_list[0] == "end":
                    print(" -- end")
                    end_flag = True
                    break
                if cmd_list[0].split(",")[0] == "1":# red
                    red_flag = True
                elif cmd_list[0].split(",")[1] == "1" :# green
                    green_flag = True

                #print("throttle: {}, steer: {}".format(throttle, steer))
                break

        #gyro.change_steer()

        #print("red,green",red_flag,green_flag)
        """if red_flag:
            #avoid_color_sign.avoidRed()
            avoid_color_sign.setBias(20)
        elif green_flag:
            #avoid_color_sign.avoidGreen()
            avoid_color_sign.setBias(-20)"""
        if True:
            #print("bias",avoid_color_sign.bias)
            gyro.straightening(20,0)
            gyro.change_steer()

            #gyro.straightening(20,avoid_color_sign.bias)


        resetSerialBuffer()
