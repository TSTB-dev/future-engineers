# ここにコードを書いてね :-)
import hub
import time
import re
from avoid_color_sign import Avoid_color_sign
from gyro import Gyro
from basic_motion import Basic_motion
print("--device init--")

while True:
    motor = hub.port.C.motor
    motor_steer = hub.port.E.motor
    ser = hub.port.D
    light_sensor = hub.port.A.device
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
basic = Basic_motion(motor_steer,motor)
def resetSerialBuffer():
    while True:
        reply = ser.read(10000)
        #print(reply)
        if reply == b"":
            break


ser_size = 13

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
    throttle = 0
    steer = 0
    rot = 0

    count = 0
    bias_roll=0

    sign_flag = 0
    last_flag = 0
    while True:
        cmd = ""
        while True:

            #time.sleep(50/1000)
            reply = ser.read(ser_size - len(cmd))
            reply = reply.decode("utf-8")
            #print("reply: ",reply)
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

            if len(cmd) >= ser_size and cmd[-1:] == "@":
                #print(cmd)
                cmd_list = cmd.split("@")
                if len(cmd_list) != 2:
                    print(len(cmd_list))
                    cmd = ""
                    continue


                steer = int(cmd_list[0].split(",")[0])
                throttle = int(cmd_list[0].split(",")[1])

                rot = int(cmd_list[0].split(",")[3])
                if (int(sign_flag) !=  int(cmd_list[0].split(",")[2]))and(sign_flag!=0):
                    last_flag=sign_flag
                sign_flag = int(cmd_list[0].split(",")[2])
                break

        if end_flag:
            print("inendflag")
            motor.brake()
            motor_steer.barke()
            break
        #標識を何も認識していない時は0で、認識している時は0以外を返すようにしている
        if  steer == 0:
            if bias_roll>=600:
                bias_roll=0
                avoid_color_sign.bias=0
            st_roll=motor.get()[0]
            gyro.straightening(30,avoid_color_sign.bias)

            en_roll=motor.get()[0]
            bias_roll+=en_roll-st_roll

            #gyro.change_steer()
        else:
            if steer > 0 :#red
                avoid_color_sign.setBias(0)
                bias_roll=0
            else: #green
                avoid_color_sign.setBias(0)
                bias_roll=0

            basic.move(throttle,steer)
        h = light_sensor.get(2)[0]
        s = light_sensor.get(2)[1]
        v = light_sensor.get(2)[2]
        blue_camera = (rot == 1)
        orange_camera = (rot == 2)
        terms_light_sensor = (h >  210-130) and ( h < 210+130) and(s > 256) and (s < 1024) and(v >= 0) and (v <= 1023)

        gyro.back_turn(40,rot)
        """
        if rot==1:
            if last_flag==0 or last_flag==1:
                print("1")
                if gyro.change_steer(20,rot)==True:
                    bias_roll=100000
            elif last_flag==2:
                print("2")
                if gyro.buck_turn(20,rot)==True:
                    bias_roll=100000
        elif rot==2:
            if last_flag==0 or last_flag==1:
                print("3")
                if gyro.back_turn(20,rot)==True:
                    bias_roll=100000
            elif last_flag==2:
                print("4")
                if gyro.change_steer(20,rot)==True:
                    bias_roll=100000
        """

        resetSerialBuffer()


