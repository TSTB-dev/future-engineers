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
#cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('H', '2', '6', '4'));
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

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
rotation_mode = ""
steer = 0
while True:
    blob_red, blob_green = {},{};
    area_red, area_green = 0, 0
    ok_blue,ok_orange = False, False
    red , green = 0, 0

    blob_red, blob_green,ok_blue,ok_orange, frame, mask_red, mask_green = color_tracking.detect_sign_area(threshold, cap)
    area_red = blob_red["area"]
    area_green = blob_green["area"]

    center_red = blob_red["center"]
    center_green = blob_green["center"]

    #print("center_red,green:{},{}".format(center_red,center_green))

    center_red_x = center_red[0]
    center_green_x = center_green[0]

    height, width, channels = frame.shape[:3]

    red_raito = area_red/(width*height)
    green_raito = area_green/(width*height)

    #print("green_raito",green_raito)
    #print("red_raito",red_raito)

    if mode == "recording":
        frame_writer.write(frame)
        #red_writer.write(mask_red)
        #green_writer.write(mask_green)

    if rotation_mode == "":# 周回の向き決定
        if ok_blue:
            rotation_mode = "blue"
        if ok_orange:
            rotation_mode = "orange"
    steer = 0
    #print("red_raito:{},green_raito:{}".format(red_raito,green_raito))
    if red_raito >= 0.015 or green_raito >= 0.015:#標識認識によるsteer値の決定
        center_frame = width/2
        if red_raito > green_raito:
            if red_raito < 0.15: #tracking
                #-70〜70で、標識に向かっていくようなsteer値を返す式
                steer = 500 * red_raito * (center_red_x-center_frame) /(width/2)
            else: #avoid
                steer =  700 * (red_raito** 1.3)
        else:
            if green_raito < 0.15: #tracking
                #-70〜70で、標識に向かっていくようなsteer値を返す式
                steer = 500 * green_raito * (center_green_x-center_frame) /(width/2)
            else: #avoid
                steer = -( 700 * (green_raito ** 1.3))
    #print("steer:",steer)

    rmode = 0
    if ok_blue and rotation_mode == "blue":# 青色認識
        rmode = 1
    elif ok_orange and rotation_mode == "orange":#オレンジ認識
        rmode = 2

    steer_int = int(steer)
    if steer_int > 120:
        steer_int = 120
    elif steer_int < -120:
        steer_int = -120
    print("steer_int:{}".format(steer_int))
    speed = 20
    #time.sleep(30/1000)


    cmd = "{:3d},{:3d},{}@".format(steer_int, speed,rmode)
    #print("write: {}".format(cmd))
    ser.write(cmd.encode("utf-8"))
    '''
    if cv2.waitKey(25) & 0xFF == ord('q'):
        print("pressd q")
        break
    '''

    for i in range (1) :#読み飛ばす処理（遅延して昔の値を取っている場合があるため）
        img = cap.read()


    end = time.perf_counter()
    elapsed_time = end-start
    if elapsed_time > 500:
        break

cv2.destroyAllWindows()
frame_writer.release()
#red_writer.release()
#green_writer.release()

ser.write("end@".encode())
