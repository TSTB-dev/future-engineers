import cv2
import os
import numpy as np
import serial
#from pylsd.lsd import lsd

def red_detect(img):
    # HSV色空間に変換
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    """
    # 赤色のHSVの値域1
    hsv_min = np.array([0,127,5])
    hsv_max = np.array([10,255,255])
    mask1 = cv2.inRange(hsv, hsv_min, hsv_max)

    # 赤色のHSVの値域2

    hsv_min = np.array([150,127,5])
    hsv_max = np.array([180,255,255])
    mask2 = cv2.inRange(hsv, hsv_min, hsv_max)
    """
    # 赤色のHSVの値域1
    hsv_min = np.array([0,200,20])
    hsv_max = np.array([10,255,255])
    mask1 = cv2.inRange(hsv, hsv_min, hsv_max)

    # 赤色のHSVの値域2

    hsv_min = np.array([170,200,20])
    hsv_max = np.array([180,255,255])
    mask2 = cv2.inRange(hsv, hsv_min, hsv_max)

    return mask1 + mask2



def green_detect(img):
    # HSV色空間に変換
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 緑色のHSVの値域
    hsv_min = np.array([45,64,30])
    hsv_max = np.array([90,255,255])
    mask1 = cv2.inRange(hsv, hsv_min, hsv_max)

    return mask1

def blue_detect(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 青のHSVの値域
    hsv_min = np.array([104,25,20])
    hsv_max = np.array([124,255,255])
    mask1 = cv2.inRange(hsv, hsv_min, hsv_max)

    return mask1

"""
def frame_lsd(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    lines = lsd(hsv)
    for i in range(lines.shape[0]):
        pt1 = (int(lines[i, 0]), int(lines[i, 1]))
        pt2 = (int(lines[i, 2]), int(lines[i, 3]))
        width = lines[i, 4]
        lsd_frame=cv2.line(src, pt1, pt2, (0, 0, 255), int(np.ceil(width / 2)))

    return lsd_frame
"""

def orange_detect(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # orengeのHSVの値域
    hsv_min = np.array([5,30,20])
    hsv_max = np.array([20,255,255])
    mask1 = cv2.inRange(hsv, hsv_min, hsv_max)

    return mask1

def analysis_blob(binary_img):
    #connectedComponentsWithStatsmはオブジェクト（連結領域）を検出するメソッド
    labels = cv2.connectedComponentsWithStats(binary_img)

    #ラベルの数（背景もラベリングされるので、オブジェクトの数はlabel[0]-1となる
    n_labels = labels[0]-1

    #起動時やオブジェクトが完全にない場合に、背景しか抽出されない場合がある
    if n_labels == 0:
        return 0

    #背景は0とラベリングされるので、最初の行を削除して格納する
    #dataにはそのラベルの {左上のx座標、左上のy座標、幅、高さ、面積}の情報が格納されている
    data = np.delete(labels[2], 0, axis=0)

    #オブジェクトの重心
    #center = np.delete(labels[3], 0, axis=0)
    #面積が最大値のラベルのインデックス
    max_index = np.argmax(data[:, 4])

    #一番大きいオブジェクトの情報を抽出
    #maxblob = {}
    #maxblob["upper_left"] = (data[:, 0][max_index], data[:, 1][max_index]) # 左上座標
    #maxblob["width"] = data[:, 2][max_index]  # 幅
    #maxblob["height"] = data[:, 3][max_index]  # 高さ
    #maxblob["area"] = data[:, 4][max_index]   # 面積（1280×720のうちのピクセル数、環境によって違うかも）
    #maxblob["center"] = center[max_index]  # 中心座標
    area = data[:, 4][max_index]
    #print(area)

    return area

def detect_sign(threshold, cap, mode="", frame_writer=None):
    #cap = cv2.VideoCapture(0)
    is_red = False
    is_green = False

    assert cap.isOpened(), "カメラを認識していません！"
    ret, frame = cap.read()

    frame = cv2.rotate(frame, cv2.ROTATE_180)
        # 赤色検出
    cv2.imshow("frame", frame)
    mask_red = red_detect(frame)
    mask_green = green_detect(frame)
    mask_blue=blue_detect(frame)
    mask_orange=orange_detect(frame)
    print("mask_size: {}".format(frame.shape))
    #mask_line=frame_lsd(frame)

    cv2.imshow("Frame", frame)
    cv2.imshow("Mask red", mask_red)
    cv2.imshow("Mask green", mask_green)
    #cv2.imshow("Mask blue", mask_blue)
    #cv2.imshow("Mask orange", mask_orange)
    #cv2.imshow("Mask line",mask_line);

    '''
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
    '''

            #フレームを記録する
    if mode == "recording":
        frame_writer.write(frame)

    area_red = analysis_blob(mask_red)
    area_green = analysis_blob(mask_green)
    area_blue = analysis_blob(mask_blue)

    #print("area red: {}, area green: {}".format(area_red, area_green))

    #赤の物体と緑の物体の大きい方の面積がthreshold以上ならフラグを立てる
    if not area_red and not area_green:
        pass
    elif area_red > area_green and area_red > threshold:
        is_red = True
    elif area_green > threshold:
        is_green = True

    #return is_red, is_green
    return is_red, is_green, frame, mask_red, mask_green

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
        #青色検出
        mask_blue = blue_detect(frame)




        # マスク画像をブロブ解析（標識と判定されたブロブ情報を取得）
        max_blob_red = analysis_blob(mask_red)
        max_blob_green = analysis_blob(mask_green)
        max_blob_blue = analysis_blob(mask_blue)


        # is_red, is_green = detect_sign(frame)

        # 結果表示
        """cv2.imshow("Frame", frame)
        cv2.imshow("Mask red", mask_red)
        cv2.imshow("Mask green", mask_green)"""
        # qキーが押されたら途中終了
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    frame_rate = 30
    size = (640, 480)
    fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    os.makedirs("../../results/", exist_ok = True)
    frame_writer = cv2.VideoWriter('../../results/after.mp4', fmt, frame_rate, size)


    WIDTH = 640
    HEIGHT = 480
    FPS = 30
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, FPS)

    #fourcc = decode_fourcc(cap.get(cv2.CAP_PROP_FOURCC))
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('B', 'G', 'R', '3'))
    fps = cap.get(cv2.CAP_PROP_FPS)
    print("fps:{}　width:{}　height:{}".format(fps, width, height))

    while True:
        detect_sign(20000, cap, mode="recording", frame_writer=frame_writer)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
    frame_writer.release()
    """
    cap = cv2.VideoCapture(0)
    print(cap.set(cv2.CAP_PROP_FPS, 40))
    print(cap.get(cv2.CAP_PROP_FPS))
    while True:
        #start = time.perf_counter()
        is_red, is_green , frame, mask_red, mask_green= detect_sign(20000, cap)
        #end = time.perf_counter()
        #print("elapsed_time: {}[us]\n".format((end-start)*1000000))"""

