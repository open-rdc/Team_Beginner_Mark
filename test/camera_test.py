import cv2
from picamera2 import Picamera2

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

try:
    while True:
        # フレームを取得
        frame = picam.capture_array()
        # RGBからOpenCV用のBGRに変換
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        # 画面表示
        cv2.imshow('Real-time Camera', frame_bgr)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    picam.stop()
    cv2.destroyAllWindows()
