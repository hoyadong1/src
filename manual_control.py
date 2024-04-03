import cv2
import numpy as np
from urllib.request import urlopen
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

ip = "192.168.137.108"
stream = urlopen("http://" + ip + ":81/stream")
buffer = b""
urlopen("http://" + ip + "/action?go=speed40")

if os.path.isdir("01_go") is False:
    os.mkdir("01_go")

if os.path.isdir("02_left") is False:
    os.mkdir("02_left")

if os.path.isdir("03_right") is False:
    os.mkdir("03_right")

go_cnt = 0
left_cnt = 0
right_cnt = 0
car_state = "stop"

while True:
    buffer += stream.read(4096)
    head = buffer.find(b"\xff\xd8")
    end = buffer.find(b"\xff\xd9")

    try:
        if head > -1 and end > -1:
            jpg = buffer[head : end + 2]
            buffer = buffer[end + 2 :]
            img = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_UNCHANGED)

            height, width, _ = img.shape
            img = img[height // 2 :, :]

            img = cv2.resize(img, (224, 224), interpolation=cv2.INTER_AREA)

            cv2.imshow("AI CAR Streaming", img)

            key = cv2.waitKey(1)
            if key == ord("q"):
                urlopen("http://" + ip + "/action?go=stop")
                break
            elif key == ord("w"):
                print("forward")
                urlopen("http://" + ip + "/action?go=forward")
                break
            elif key == ord("a"):
                print("left")
                urlopen("http://" + ip + "/action?go=left")
                break
            elif key == ord("d"):
                print("right")
                urlopen("http://" + ip + "action?go=right")
                break
            elif key == ord("s"):
                print("backward")
                urlopen("http://" + ip + "/action?go=backward")
                break
            elif key == ord("A"):
                print("turn left")
                urlopen("http://" + ip + "/action?go=turn_left")
                break
            elif key == ord("D"):
                print("turn right")
                urlopen("http://" + ip + "/action?go=turn_right")
                break
            elif key == 32:
                print("stop")
                urlopen("http://" + ip + "/action?go=stop")
                break
            elif key == ord("1"):
                print("40 speed")
                urlopen("http://" + ip + "/action?go=speed40")
                break
            elif key == ord("2"):
                print("50 speed")
                urlopen("http://" + ip + "/action?go=speed50")
                break
            elif key == ord("3"):
                print("60 speed")
                urlopen("http://" + ip + "/action?go=speed60")
                break
            elif key == ord("4"):
                print("80 speed")
                urlopen("http://" + ip + "/action?go=speed80")
                break
            elif key == ord("5"):
                print("100 speed")
                urlopen("http://" + ip + "/action?go=speed100")
                break

    except:
        print("error")
        pass

urlopen("http://" + ip + "/action?go=stop")
cv2.destroyAllWindows()
