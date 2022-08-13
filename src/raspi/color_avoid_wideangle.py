
# カラー検出及び制御量の算出と制御
import serial
import time
import color_tracking
import cv2
import os
import numpy as np

ser = serial.Serial('/dev/ttyAMA1', 115200)
throttle = 20

data_dir = "/home/pi/WRO2022/data"
save_dir = os.path.join(data_dir, "train")
SAVE_FPS = 1

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
WIDTH =  160*2
HEIGHT = 120*2

cap = cv2.VideoCapture(0)
assert cap.isOpened(), "カメラを認識していません！"
#cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('H', '2', '6', '4'));
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
values = ""
ser.reset_input_buffer()

#cap.set(cv2.CAP_PROP_GAIN,-1)

green = 0
red = 0
count = 0
_id = 0
#mode = "get_img"
mode = ""
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
sign_flag = 0
while True:
    end = time.perf_counter()
    elapsed_time = end - start
    blob_red, blob_green = {},{};
    area_red, area_green = 0, 0
    ok_blue,ok_orange = False, False
    blue_center_y, orange_center_y = 0,0
    red , green = 0, 0
    sign_flag = 0
    wall_right, wall_left = False, False
    black_right_raito, black_left_raito = 0,0
    blob_red, blob_green,ok_blue,ok_orange,blue_center_y,orange_center_y, frame, mask_red, mask_green, cliped_frame,black_right_raito,black_left_raito = color_tracking.detect_sign_area(threshold, cap)

    if black_right_raito > 0.7:
        wall_right = True
    elif black_left_raito > 0.7:
        wall_left = True
    print("black_left,blue_center_y",black_left_raito,blue_center_y)
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

    if mode == "get_img" and elapsed_time > 1/SAVE_FPS:
        id_path = "{:06}.png".format(_id)
        frame_path = os.path.join(save_dir, id_path)
        cv2.imwrite(frame_path, frame)
        _id += 1
        elapsed_time = 0

    if rotation_mode == "":# 周回の向き決定
        if ok_blue:
            rotation_mode = "blue"
        if ok_orange:
            rotation_mode = "orange"

    steer = 0
    max_area = 0.4
    speed = 50
    rmode = 0
    #print("red_raito,green_raito:",red_raito,green_raito)
    if red_raito >= 0.0025 or green_raito >= 0.0025:#標識認識によるsteer値の決定
        center_frame = width/2
        if red_raito > green_raito:
            if red_raito < 0.4: #tracking past:0.02
                sign_flag = 1
                if rotation_mode == "orange" and center_red_x/width < 0.1:
                    sign_flag = 0
                    if green_raito > 0.001:
                        sign_flag = 2
                distance = red_raito/max_area
                wide = (center_red_x/width)-0.5 + 0.2

                center_raito_red = (center_red_x/width)

                #if red_raito < 0.006:
                #    wide = wide - 0.1
                #print("center_raito_red,red_raito",center_raito_red,red_raito)
                if wide > 1:
                    wide = 1
                """
                if center_raito_red > 0.2:
                    if red_raito > 0.02:
                        steer = 120
                    elif red_raito > 0.015:
                        steer = 70
                    elif red_raito > 0.01:
                        steer = 50
                    elif red_raito > 0.001:
                        steer = 30
                    else:
                        steer = 20
                    if center_raito_red > 0.8:
                        steer = steer * 1.5
                    elif center_raito_red> 0.6:
                        steer = steer * 1.2
                    else:
                        steer = steer * 0.8
                elif center_raito_red <= 0.2:
                    if red_raito > 0.02:
                        steer = 50
                    elif red_raito > 0.01:
                        steer = -10
                    else:
                        steer = 0
                if center_raito_red > 0.3 and (rotation_mode == "orange" or rotation_mode == ""):
                    if red_raito < 0.018 and black_right_raito > 0.6:
                        #sign_flag = 3
                        steer = -80
                        speed = 30
                """
                steer = (15 * 4 ) / max_area * (90-(np.arccos(wide * distance) * 180 )/ np.pi)

                #print("before_steer,center_red_x/width : ",steer,center_red_x/width)
                #避ける方向と逆方向に曲がる必要がある時は緩和する
                #0でもよさそう
                if red_raito < 0.003:
                    steer = steer * 0.5
                if steer < 0:
                    if center_red_x/width < 0.2:
                        steer = 0
                    if (red_raito > 0.03 and center_red_x/width > 0.3) or (red_raito > 0.04 and center_red_x/width > 0.05):
                        steer = 60
                    elif red_raito > 0.017 or (red_raito > 0.01 and center_red_x/width < 0.3):
                        steer = 0
                    elif red_raito > 0.01:
                        steer = steer * 0.5
                    else:
                        steer = (steer * 0.8)

                elif steer > 0:
                    if red_raito > 0.015:
                        steer = steer * 1.6
                    elif red_raito > 0.006:
                        steer = steer * 1.6
                    if center_red_x/width < 0.2:
                        steer = steer * 1.3

                #if red_raito > 0.017 and steer < 0 and center_red_x/width > 0.2:
                    #steer = 50

                #if red_raito > 0.017 and steer >= 1 and steer < 30:
                    #steer = steer * 2
                if wall_right:
                    steer = -80
                elif wall_left:
                    steer = 80
                if red_raito > 0.15: #avoid
                    #steer =  1700 * (red_raito** 1.3)
                    steer = 120
                    speed = 30


                #0にするとstraightingになるので、1を送る
                if int(steer) == 0:
                    steer = 1

        else:
            if green_raito < 0.4: #tracking past:0.02
                sign_flag = 2
                distance = green_raito/max_area
                #print("center_green_x/width:",center_green_x/width)
                if rotation_mode == "blue" and center_green_x/width > 0.9:
                    sign_flag = 0
                    if red_raito > 0.001:
                        sign_flag = 1
                wide = (center_green_x/width)-0.5 - 0.2

                center_raito_green = (center_green_x/width)
                print("green_raito:",green_raito)
                """if center_raito_green < 0.8:
                    if green_raito > 0.02:
                        steer = -120
                    elif green_raito > 0.015:
                        steer = -70
                    elif green_raito > 0.01:
                        steer = -50
                    elif green_raito > 0.001:
                        steer = -30
                    else:
                        steer = -20
                    if center_raito_green < 0.2:
                        steer = steer * 1.5
                    elif center_raito_green < 0.4:
                        steer = steer * 1.2
                    else:
                        steer = steer * 0.8
                elif center_raito_green >= 0.8:
                    if green_raito > 0.02:
                        steer = -50
                    elif green_raito > 0.018:
                        steer = 0
                    else:
                        steer = 10

                #if green_raito < 0.006:
                    #wide = wide + 0.1
                if center_raito_green < 0.7 and (rotation_mode == "blue" or rotation_mode == ""):
                    if green_raito < 0.018 and black_left_raito > 0.5:
                        #sign_flag =3
                        speed = 30
                        steer = 80


                if wide  < -1:
                    wide = -1

                """
                steer = 15 * 4 / max_area * (90-(np.arccos(wide * distance) * 180 )/ np.pi)
                if green_raito < 0.003:
                    steer = steer * 0.5
                #避ける方向と逆方向に曲がる必要がある時は緩和する
                #0でもよさそう
                if steer > 0:
                    if center_green_x/width > 0.8:
                        steer = 0
                    if green_raito > 0.03 and center_green_x/width <= 0.7:
                        steer = -60
                    elif green_raito > 0.017 or (green_raito > 0.01 and center_green_x/width > 0.7):
                        steer = 0
                    elif red_raito > 0.01:
                        steer = steer * 0.5
                    else:
                        steer = (steer * 0.8)

                elif steer < 0:
                    if green_raito > 0.015:
                        steer = steer * 1.6
                    elif green_raito > 0.006:
                        steer = steer * 1.6
                    if center_green_x/width > 0.8:
                        steer = steer * 1.3

                #近づきすぎた時の緊急回避（あんまり機能してない）

                #if green_raito > 0.017 and steer > 0 and center_green_x/width < 0.8:
                 #   steer = -50

                #if green_raito > 0.01 and steer < 0 and center_green_x/width <-0.3:
                   # steer = 0


                #if green_raito > 0.017 and steer <= -1 and steer > -30:
                    #steer = steer * 2
                #if green_raito > 0.017 and steer >=1 and steer <=20:
                    #steer = steer * 2
                if wall_right:
                    steer = -80
                elif wall_left:
                    steer = 80

                if green_raito > 0.15: #avoid
                    #steer = -( 1700 * (green_raito ** 1.3))
                    steer = -120
                    speed = 30


                if int(steer) == 0:
                    steer = -1

    if wall_right:
        if rotation_mode == "blue":
            sign_flag = 1
            steer = -80
        else:
            sign_flag = 2
            steer = -80
    elif wall_left:
        if rotation_mode == "blue":
            sign_flag = 2
            steer = 80
        else:
            sign_flag = 1
            steer = 80
    if ok_blue and rotation_mode == "blue":# 青色認識
        rmode = 1
    elif ok_orange and rotation_mode == "orange":#オレンジ認識
        rmode = 2

    steer_int = int(steer)
    if steer_int > 120:
        steer_int = 120
    elif steer_int < -120:
        steer_int = -120

    cmd = "{:4d},{:3d},{},{}@".format(steer_int, speed,sign_flag,rmode)
    print("write: {}".format(cmd))
    ser.write(cmd.encode("utf-8"))



    """if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows(
        ser.write(cmd.encode("utf-8"))
        print("pressd q")
        break"""

    #print(cmd)
    for i in range (1) :#読み飛ばす処理（遅延して昔の値を取っている場合があるため）
       img = cap.read()


    end = time.perf_counter()
    elapsed_time = end-start


cv2.destroyAllWindows()
frame_writer.release()
#red_writer.release()
#green_writer.release()

ser.write("end@".encode())
