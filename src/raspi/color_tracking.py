
import cv2
import numpy as np
import time
import serial

def red_detect(img):
    # HSV色空間に変換
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 赤色のHSVの値域1
    hsv_min = np.array([0,80,30])
    hsv_max = np.array([0,255,255])
    mask1 = cv2.inRange(hsv, hsv_min, hsv_max)

    # 赤色のHSVの値域2

    hsv_min = np.array([150,80,30])
    hsv_max = np.array([180,255,255])
    mask2 = cv2.inRange(hsv, hsv_min, hsv_max)
    return mask1 + mask2


def black_detect(img):
    # HSV色空間に変換
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 黒色のHSVの値域
    hsv_min = np.array([0,0,0])
    hsv_max = np.array([180,255,100])
    mask1 = cv2.inRange(hsv, hsv_min, hsv_max)

    return mask1
def red_detect_rgb(img):
    hsv_min = np.array([50,0,0])
    hsv_max = np.array([255,50,50])
    mask1 = cv2.inRange(img, hsv_min, hsv_max)

    return mask1

def green_detect(img):
    # HSV色空間に変換
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 緑色のHSVの値域

    hsv_min = np.array([65,140,30])
    hsv_max = np.array([90,255,255])

    #hsv_min = np.array([30,100,30])
    #hsv_max = np.array([60,255,255])

    #hsv_min = np.array([60,100,45])
    #hsv_max = np.array([90,255,255])

    mask1 = cv2.inRange(hsv, hsv_min, hsv_max)

    return mask1

def orange_detect(img):
    # HSV色空間に変換
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # orangeのHSVの値域
    hsv_min = np.array([0,40,20])
    hsv_max = np.array([30,255,255])
    mask1 = cv2.inRange(hsv, hsv_min, hsv_max)

    return mask1

def blue_detect(img):
    # HSV色空間に変換
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #buleHSVの値域
    hsv_min = np.array([100,38,60])
    hsv_max = np.array([120,255,200])
    mask1 = cv2.inRange(hsv, hsv_min, hsv_max)

    return mask1

def analysis_blob(binary_img):
    maxblob = {}
    #connectedComponentsWithStatsmはオブジェクト（連結領域）を検出するメソッド
    labels = cv2.connectedComponentsWithStats(binary_img)

    #ラベルの数（背景もラベリングされるので、オブジェクトの数はlabel[0]-1となる
    n_labels = labels[0]-1

    #起動時やオブジェクトが完全にない場合に、背景しか抽出されない場合がある
    if n_labels == 0:
        #例外の時、max_blobに値を突っ込んでおいた方が都合がいい
        #areaが0なので何も起こらない
        maxblob["upper_left"] = (0,0) # 左上座標
        maxblob["width"] = 0
        maxblob["height"] = 0
        maxblob["area"] = 0
        maxblob["center"] = (0,0)
        return maxblob

    #背景は0とラベリングされるので、最初の行を削除して格納する
    #dataにはそのラベルの {左上のx座標、左上のy座標、幅、高さ、面積}の情報が格納されている
    data = np.delete(labels[2], 0, axis=0)

    #オブジェクトの重心
    center = np.delete(labels[3], 0, axis=0)
    #面積が最大値のラベルのインデックス
    max_index = np.argmax(data[:, 4])


    #一番大きいオブジェクトの情報を抽出

    #maxblob["upper_left"] = (data[:, 0][max_index], data[:, 1][max_index]) # 左上座標
    #maxblob["width"] = data[:, 2][max_index]  # 幅
    #maxblob["height"] = data[:, 3][max_index]  # 高さ
    maxblob["area"] = data[:, 4][max_index]   # 面積（1280×720のうちのピクセル数、環境によって違うかも）
    maxblob["center"] = center[max_index]  # 中心座標
    area = data[:, 4][max_index]
    #print(area)

    return maxblob
def analysis_blob_line(binary_img):
    max_width_blob = {}
    #connectedComponentsWithStatsmはオブジェクト（連結領域）を検出するメソッド
    labels = cv2.connectedComponentsWithStats(binary_img)

    #ラベルの数（背景もラベリングされるので、オブジェクトの数はlabel[0]-1となる
    n_labels = labels[0]-1

    #起動時やオブジェクトが完全にない場合に、背景しか抽出されない場合がある
    if n_labels == 0:
        #例外の時、max_blobに値を突っ込んでおいた方が都合がいい
        #areaが0なので何も起こらない
        max_width_blob["upper_left"] = (0,0) # 左上座標
        max_width_blob["width"] = 0
        max_width_blob["height"] = 0
        max_width_blob["area"] = 0
        max_width_blob["center"] = (0,0)
        return max_width_blob

    #背景は0とラベリングされるので、最初の行を削除して格納する
    #dataにはそのラベルの {左上のx座標、左上のy座標、幅、高さ、面積}の情報が格納されている
    data = np.delete(labels[2], 0, axis=0)

    #オブジェクトの重心
    center = np.delete(labels[3], 0, axis=0)
    #面積が最大値のラベルのインデックス
    max_index = np.argmax(data[:, 4])

    #横幅が最大値のインデックス
    max_width_index = np.argmax(data[:, 2])
    height, width = binary_img.shape[:3]
    #一番大きいオブジェクトの情報を抽出

    max_width_blob["upper_left"] = (data[:, 0][max_index], data[:, 1][max_index]) # 左上座標
    max_width_blob["width"] = data[:, 2][max_index]  # 幅
    max_width_blob["height"] = data[:, 3][max_index]  # 高さ
    max_width_blob["area"] = data[:, 4][max_index]   # 面積（1280×720のうちのピクセル数、環境によって違うかも）
    max_width_blob["center"] = center[max_index]  # 中心座標
    area = data[:, 4][max_index]

    #print("n_labels:" ,n_labels)
    #print("maxwidthblob_width:" ,data[:, 2][max_width_index])
    #print("maxwidthblob_upper_left:",(data[:, 0][max_width_index], data[:, 1][max_width_index]))
    #time.sleep(1)
    #print(area)
    return max_width_blob

def detect_sign(threshold, cap, mode=""):

    is_red = False
    is_green = False

    ok_blue = False
    ok_orange = False

    assert cap.isOpened(), "カメラを認識していません！"
    ret, f = cap.read()

    frame = cv2.rotate(f, cv2.ROTATE_180)
        # 赤色検出

    mask_red = red_detect(frame)
    mask_green = green_detect(frame)
    mask_blue = blue_detect(frame)
    mask_orange = orange_detect(frame)

    """cv2.imshow("Frame", frame)
    cv2.imshow("Mask red", mask_red)
    cv2.imshow("Mask green", mask_green)"""



    """if cv2.waitKey(1) & 0xFF == ord('q'):

        cv2.destroyAllWindows()"""

    area_red = analysis_blob(mask_red)
    area_green = analysis_blob(mask_green)
    blob_orange = analysis_blob_line(mask_orange)
    blob_blue = analysis_blob_line(mask_blue)


    #print("area red: {}, area green: {}".format(area_red, area_green))

    #赤の物体と緑の物体の大きい方の面積がthreshold以上ならフラグを立てる
    if not area_red and not area_green:
        pass
    elif area_red > area_green and area_red > threshold:
        is_red = True
    elif area_green > threshold:
        is_green = True

    height, width, channels = frame.shape[:3]

    #print(blob_blue["upper_left"])
    if blob_blue != 0:
        blue_y = blob_blue["upper_left"][1]
        blue_width = blob_blue["width"]

        if blue_width < 100 :
            pass
        elif blue_y > height * 0.8:
            ok_blue = True
    if blob_orange != 0:
        orange_y = blob_orange["upper_left"][1]
        orange_width = blob_orange["width"]
        if orange_width < 100 :
            pass
        elif orange_y > height * 0.8:
            ok_orange = True

    """cv2.imshow("Frame", frame)
    cv2.imshow("Mask red", mask_red)
    cv2.imshow("Mask green", mask_green)
    cv2.imshow("Mask orange",mask_orange)
    cv2.imshow("Mask blue",mask_blue)"""
    #return is_red, is_green
    return is_red, is_green,ok_blue,ok_orange ,frame, mask_red, mask_green

def main():
    # カメラのキャプチャ
    cap = cv2.VideoCapture(0)
    while(cap.isOpened()):
        _, f = cap.read()
        frame = cv2.rotate(f, cv2.ROTATE_180)
        # 赤色検出
        mask_red = red_detect(frame)
        #緑色検出
        mask_green = green_detect(frame)

        mask_blue = blue_detect(frame)
        mask_orange = orange_detect(frame)

        # マスク画像をブロブ解析（標識と判定されたブロブ情報を取得）
        max_blob_red = analysis_blob(mask_red)
        max_blob_green = analysis_blob(mask_green)

        # is_red, is_green = detect_sign(frame)
        max_blob_orange = analysis_blob_line(mask_orange)
        # 結果表示
        cv2.imshow("Frame", frame)
        #cv2.imshow("Mask red", mask_red)
        #cv2.imshow("Mask green", mask_green)
        #cv2.imshow("Mask orange",mask_orange)
        #cv2.imshow("Mask blue",mask_blue)
        # qキーが押されたら途中終了
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def detect_sign_area(threshold, cap, mode=""):#標識の面積を返すdetect_sign（面積によって動作を変えたいため）

    is_red = False
    is_green = False

    ok_blue = False
    ok_orange = False

    clip_ratio = 0.375 #clip in the top of image for the specific ratio
    assert cap.isOpened(), "カメラを認識していません！"
    ret, frame = cap.read()
    clip_threshold = int(clip_ratio*frame.shape[0])
    cliped_frame = frame[clip_threshold:,:,:]
    frame = cv2.resize(frame, dsize=(160, 120))
    #frame = cv2.rotate(f, cv2.ROTATE_180)
    #frame = cv2.rotate(f, cv2.ROTATE_180)
        # 赤色検出

    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #frame_hsv[:, :, (0)] = frame_hsv[:, :, (0)]
    #frame_hsv[:, :, (1)] = np.clip(frame_hsv[:, :, (1)]*1.5,0,255)
    #frame_hsv[:, :, (2)] = np.clip(frame_hsv[:, :, (2)]*1.9,0,255)
    frame = cv2.cvtColor(frame_hsv, cv2.COLOR_HSV2BGR)
    #frame[:,:,(1)] = np.clip(frame[:,:,(1)] * 1.5,0,255)
    """
    gamma = 0.5
    gamma_cvt = np.zeros((256,1), dtype=np.uint8)
    for i in range(256):
        gamma_cvt[i][0] = 255*(float(i)/255)**(1.0/gamma)
    frame = cv2.LUT(frame,gamma_cvt)
    """
    mask_red = red_detect(frame)
    mask_green = green_detect(frame)
    mask_blue = blue_detect(frame)
    mask_orange = orange_detect(frame)
    mask_black = black_detect(frame)
    mask_black_left = black_detect(frame)
    mask_black_right = black_detect(frame)




    """cv2.imshow("Frame", frame)
    cv2.imshow("Mask red", mask_red)
    cv2.imshow("Mask green", mask_green)"""

    height, width, channels = frame.shape[:3]
    mask_red[0:int(2 * height/5),:] = 0
    mask_green[0:int(2 * height/5),:] = 0
    mask_blue[0:int(3 * height/5),:] = 0
    mask_orange[0:int(3 * height/5),:] = 0

    mask_black_left[0:int(height/2),:] = 0
    mask_black_left[int(height/2):int(height),int(width/2):int(width)] = 0

    mask_black_right[0:int(height/2),:] = 0
    mask_black_right[int(height/2):int(height),0:int(width/2)] = 0

    """if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()"""


    blob_red = analysis_blob(mask_red)
    blob_green = analysis_blob(mask_green)
    blob_orange = analysis_blob_line(mask_orange)
    blob_blue = analysis_blob_line(mask_blue)
    blob_brack_right = analysis_blob_line(mask_black_right)
    blob_brack_left = analysis_blob_line(mask_black_left)


    black_left_area = blob_brack_left["area"]
    black_right_area = blob_brack_right["area"]

    black_right_raito = black_right_area * 4 / (width * height)
    black_left_raito = black_left_area * 4 / (width * height)

    #print("right_raito,left_raito:",black_right_raito,black_left_raito)
    wall_right,wall_left = False,False
    if black_right_raito > 0.7:
        wall_right = True
    elif black_left_raito > 0.7:
        wall_left = True

    rcx = blob_red["center"][0]
    rcy = blob_red["center"][1]
    gcx = blob_green["center"][0]
    gcy = blob_green["center"][1]
    #cv2.circle(frame,(int(rcx),int(rcy)),15,(0,0,255))
    #cv2.circle(frame,(int(gcx),int(gcy)),15,(0,255,0))

    #print("area red: {}, area green: {}".format(area_red, area_green))

    #赤の物体と緑の物体の大きい方の面積がthreshold以上ならフラグを立てる
    area_red = blob_red["area"]
    area_green = blob_green["area"]
    if not area_red and not area_green:
        pass
    elif area_red > area_green and area_red > threshold:
        is_red = True
    elif area_green > threshold:
        is_green = True

    height, width, channels = frame.shape[:3]

    #print(blob_blue["upper_left"])

    #print("areablue,orange",blob_blue["area"]/(width*height),blob_orange["area"]/(width*height))

    blue_center_y = 0
    orange_center_y = 0
    if blob_blue != 0:
        blue_center = blob_blue["center"]
        blue_area = blob_blue["area"]
        if blue_area/(height * width) > 0.005 :
            if blue_center[1] > 3 * height / 4:
                ok_blue = True
            blue_center_y = blue_center[1]/height
        #print("blue_area,center:",blue_area,blue_center)
    if blob_orange != 0:
        orange_center = blob_orange["center"]
        orange_area = blob_orange["area"]
        if orange_area/(width * height) > 0.005 :
            if orange_center[1] > 3 * height / 4:
                ok_orange = True
            orange_center_y = orange_center[1]/height
        #print("orange_area,center:",orange_area,orange_center)
    cv2.imshow("Frame", frame)
    cv2.imshow("Mask red", mask_red)
    cv2.imshow("Mask green", mask_green)
    cv2.imshow("Mask orange",mask_orange)
    cv2.imshow("Mask blue",mask_blue)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
    cv2.imshow("Mask black",mask_black)
    #cv2.imshow("Mask black left",mask_black_left)
    #cv2.imshow("Mask black right",mask_black_right)
    #return is_red, is_green

    return blob_red, blob_green,ok_blue,ok_orange ,blue_center_y,orange_center_y,frame, mask_red, mask_green, cliped_frame,black_right_raito,black_left_raito
if __name__ == '__main__':
    #cap = cv2.VideoCapture(0)
    main()
    #while True:
    #    detect_sign(20000, cap)
    """
    cap = cv2.VideoCapture(0)
    print(cap.set(cv2.CAP_PROP_FPS, 40))
    print(cap.get(cv2.CAP_PROP_FPS))
    while True:
        #start = time.perf_counter()
        is_red, is_green , frame, mask_red, mask_green= detect_sign(20000, cap)
        #end = time.perf_counter()
        #print("elapsed_time: {}[us]\n".format((end-start)*1000000))"""
