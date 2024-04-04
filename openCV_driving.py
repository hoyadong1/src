import cv2
import numpy as np
from urllib.request import urlopen
import threading

ip = "192.168.137.121"
stream = urlopen("http://" + ip + ":81/stream")
buffer = b""
urlopen("http://" + ip + "/action?go=speed40")

imager_flag = 0


def image_process_thread():
    global image_flag, car_state
    while True:
        if imager_flag == 1:
            if car_state == "go":
                urlopen("http://" + ip + "/action?go=forward")
            elif car_state == "right":
                urlopen("http://" + ip + "/action?go=right")
            elif car_state == "left":
                urlopen("http://" + ip + "/action?go=left")

            imager_flag = 0


daemon_thread = threading.Thread(target=img_process_thread)
daemon_thread.daemon = True
daemon_thread.start()


car_state = "go"
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

            lower_bound = np.array([0, 0, 0])
            upper_bound = np.array([255, 255, 80])
            mask = cv2.inRange(img, lower_bound, upper_bound)

            cv2.imshow("mask", mask)

            M = cv2.moments(mask)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["01"] / M["m00"])
            else:
                cX, cY = 0, 0

            center_offset = width // 2 - cX

            cv2.circle(img, (cX, cY), 10, (0, 255, 0), -1)
            cv2.imshow("AI CAR Streaming", img)

            if center_offset > 10:
                print("right")
                car_state = "right"
            elif center_offset < -10:
                print("left")
                car_state = "left"
            else:
                print("forward")
                car_state = "go"

            imager_flag = 1

            key = cv2.waitKey(1)
            if key == ord("q"):
                urlopen("http://" + ip + "/action?go=stop")
                break

    except:
        print("error")
        pass


urlopen("http://" + ip + "/action?go=forward")
cv2.destroyWindow()
