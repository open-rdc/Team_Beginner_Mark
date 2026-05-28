import cv2
from picamera2 import Picamera2
import numpy as np
import math
import serial
import time

serial = serial.Serial('/dev/ttyACM0', 115200,timeout=1)
time.sleep(2)

try:
    # カメラの初期化
    try:
        picam = Picamera2()
        # メイン設定：プレビュー用のサイズを指定
        config = picam.create_preview_configuration(main={"size": (640, 480)})
        picam.configure(config)
        picam.start()
        print("カメラが正常に起動しました！終了するには 'q' キーを押してください。")
    except Exception as e:
        print(f"カメラの起動に失敗しました: {e}")
        exit()

    while True:
            # フレームを取得
            frame = picam.capture_array()
            #ノイズ消し
            bokasi = cv2.GaussianBlur(frame,(11,11),0)

            #hsv色空間に変換
            hsv = cv2.cvtColor(bokasi,cv2.COLOR_RGB2HSV)

            #赤色認識
            lower_red1 = np.array([0, 100, 100]) #0  100  100
            upper_red1 = np.array([30, 255, 255]) # 10  255 255
            mask1 = cv2.inRange(hsv, lower_red1, upper_red1)

            lower_red2 = np.array([150, 100, 100]) #150
            upper_red2 = np.array([180, 255, 255])
            mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

            mask_red = mask1 + mask2

            outline_red, _ = cv2.findContours(mask_red.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            #青色認識
            lower_blue = np.array([86, 100, 100])
            upper_blue = np.array([125, 255, 255])
            mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

            outline_blue, _ = cv2.findContours(mask_blue.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            #黃色認識
            lower_yellow = np.array([26, 100, 100])
            upper_yellow = np.array([35, 255, 255])
            mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)

            outline_yellow, _ = cv2.findContours(mask_yellow.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if len(outline_red) > 0 or len(outline_blue) > 0 or len(outline_yellow) > 0:
                area_red = cv2.contourArea(max(outline_red, key=cv2.contourArea)) if len(outline_red) > 0 else 0
                area_blue = cv2.contourArea(max(outline_blue, key=cv2.contourArea)) if len(outline_blue) > 0 else 0
                area_yellow = cv2.contourArea(max(outline_yellow, key=cv2.contourArea)) if len(outline_yellow) > 0 else 0
                max_area = max(area_red, area_blue, area_yellow)
                #面積が大きい輪郭取得
                if max_area == area_red and area_red > 0:
                    c = max(outline_red, key=cv2.contourArea)
                    color_number = 1
                elif max_area == area_blue and area_blue > 0:
                    c = max(outline_blue, key=cv2.contourArea)
                    color_number = 2
                elif max_area == area_yellow and area_yellow > 0:
                    c = max(outline_yellow, key=cv2.contourArea)
                    color_number = 3
                #面積がある程度大きい場合のみ枠出現
                if cv2.contourArea(c) > 500:
                    #外接する長方形の座標取得
                    x,y,w,h = cv2.boundingRect(c)
                    area = cv2.contourArea(c)
                    framelength = cv2.arcLength(c, True)
                    circlecheck = (4*math.pi*area)/(framelength*framelength)
                    #graphic_area = (w/2)*(w/2)*math.pi
                    #circlecheck_ver2 = math.isclose(graphic_area, area,rel_tol=0.9)
                    #(((x + (w/2)), y),(x,(y + (h/2))))
                    #if math.isclose((center - (x,(y + (h/2)))), (((x + w), (y +(h/2))) - center),abs_tol = 1e-5):
                    #円かどうかチェック
                    if circlecheck > 0.6:    #_ver2 == True:
                        if color_number == 1:
                            #元の画像に緑の枠描画
                            cv2.rectangle(frame, (x, y),(x + w, y + h), (0, 255, 0), 2)    
                            #文字
                            cv2.putText(frame, "RED DETECTED",(x, y - 10),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,255,0),2)
                            print('red')
                            serial.write(b'1')

                        elif color_number == 2:
                            #元の画像に緑の枠描画
                            cv2.rectangle(frame, (x, y),(x + w, y + h), (0, 255, 0), 2)    
                            #文字
                            cv2.putText(frame, "BLUE DETECTED",(x, y - 10),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,0,0),2)
                            print('blue')
                            serial.write(b'2')

                        elif color_number == 3:
                            #元の画像に緑の枠描画
                            cv2.rectangle(frame, (x, y),(x + w, y + h), (0, 255, 0), 2)    
                            #文字
                            cv2.putText(frame, "YELLOW DETECTED",(x, y - 10),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,0,255),2)
                            print('yellow')
                            serial.write(b'3')
                    else:
                        print('nothing_ball')
                        serial.write(b'4')
                else:
                    print('small_size')
                    serial.write(b'5')
        
            else:
                print('nothing_color')
                serial.write(b'6')


            #画面表示
            true_color_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            cv2.imshow("Original Camera Feed", true_color_frame)
            #if color_number = 1:
            all_mask = mask_red + mask_blue + mask_yellow
            cv2.imshow("color_Mask", all_mask)
            # elif color_number = 2:
            #cv2.imshow("")

        
            #qでループ抜け
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    #後片付け
    picam.stop()
    cv2.destroyAllWindows()

except KeyboardInterrupt:
    print("stop")
    serial.close()
