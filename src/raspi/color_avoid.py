# カラー検出及び制御量の算出と制御
import serial
import time
import color_tracking
import cv2
import os

ser = serial.Serial('/dev/ttyAMA1', 115200)
throttle = 20

time.sleep(1)

def avoid_object(detect_red, detect_green):
    if detect_red:
        steer = 20
    elif detect_green:
        steer = -20
    else:
        steer = 0

    return throttle, steer

def distance_controll(distance):
    steer=int((distance/2)-10)
    if steer>10:
        steer=10
        #print(steer)
        #time.sleep(1)
    return throttle, steer


print("--waiting SPIKE--")
threshold = 10000#回避動作を開始する画像中の物体の面積
steer = 0
cap = cv2.VideoCapture(0)
values = ""
ser.reset_input_buffer()

green = 0
red = 0
count = 0
mode = "recording"

frame_rate = 10
size = (640, 480)
fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
os.makedirs("../../results/", exist_ok = True)
frame_writer = cv2.VideoWriter('../../results/frame.mp4', fmt, frame_rate, size)
#red_writer = cv2.VideoWriter('../../results/red.mp4', fmt, frame_rate, size)
#green_writer = cv2.VideoWriter('../../results/green.mp4', fmt, frame_rate, size)

start = time.perf_counter()
while True:
    is_red, is_green = 0, 0
    ok_blue,ok_orange = False, False
    red , green = 0, 0
    is_red, is_green,ok_blue,ok_orange, frame, mask_red, mask_green = color_tracking.detect_sign(threshold, cap)

    if is_red:
        red = 1
    if is_green:
        green = 1

    print("ok_blue:",ok_blue)
    print("ok_orange",ok_orange)
    time.sleep(30/1000)
    if mode == "recording":
        frame_writer.write(frame)
        #red_writer.write(mask_red)
        #green_writer.write(mask_green)

    cmd = "{},{}@".format(red, green)
    print("write: {}".format(cmd))
    ser.write(cmd.encode("utf-8"))
    '''
    if cv2.waitKey(25) & 0xFF == ord('q'):
        print("pressd q")
        break
    '''
    end = time.perf_counter()
    elapsed_time = end-start
    if elapsed_time > 500:
        break

cv2.destroyAllWindows()
frame_writer.release()
#red_writer.release()
#green_writer.release()

ser.write("end@".encode())
