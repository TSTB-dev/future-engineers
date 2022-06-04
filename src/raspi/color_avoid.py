# ここにコードを書いてね :-)
# カラー検出及び制御量の算出と制御
import serial
import time
import color_tracking
import cv2

ser = serial.Serial('/dev/ttyAMA1', 115200)
speed = 50
#this function calculate throttle and steering using color detection.
#If object is detected, turn left
def avoid_object(detect_red, detect_green, speed, steer, correct_flag):
    throttle = speed
    if steer and correct_flag:#車が直前に曲がっていて、それが方向修正でないときに方向修正する
        correct_flag = True
        return throttle, -steer, correct_flag
    if detect_red:
        steer = 15
    elif detect_green:
        steer = -15
    else:
        steer = 0
    return throttle, steer, correct_flag

print("--waiting SPIKE--")
threshold = 30000#回避動作を開始する画像中の物体の面積
correct_flag = True
steer = 0

while True:

    detect_red, detect_green = color_tracking.detect_sign(threshold)
    throttle, steer, correct_flag = avoid_object(detect_red, detect_green, speed, steer, correct_flag)
    #方向を修正したらcorrect_flagを立て、それ以降ステアリングが０になるまで方向は修正しない
    if steer:
        correct_flag = False #ステアリングが０以外のとき、方向は修正しない
    else:
        correct_flag = True #ステアリングが０になったとき、correct_flagを再度立てる

    cmd = "{:3d},{:3d}@".format(throttle, steer)
    print("write: {}".format(cmd))
    ser.write(cmd.encode("utf-8"))
    #time.sleep(100/1000)

ser.write("end@".encode())

