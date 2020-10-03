from detector.detector import Detector
from settings.settings import Values
from camera.camera import Camera
from imageStream.imageStream import ImageStream
from ImageWindow.ImageWindow import ImageWindow
from PIDs.PIDs import PIDs
import cv2
import time


if __name__ == '__main__':
    detector = Detector(Values.MODEL_PATH, Values.LABEL_PATH)
    camera = Camera()
    time.sleep(1)
    imageWindow = ImageWindow()
    imageWindow.show()
    pids = PIDs(imageWindow)       #pewnie beda zle wartosci na wyjsciu do dopracowania

    if Values.SEND_IMAGES_WIFI:
        imageStream = ImageStream()

    i = 0
    try:
        while True:
            #i += 1
            name = "images/" + "4.JPG"
            frame = cv2.imread(name)
            frame = cv2.resize(frame, (640, 480))
            #frame = camera.get_frame()
            mid, ratio = detector.detect(frame)         # mid liczony od: lewy gorny rog

            pids.update(mid, ratio)
            imageWindow.update_image(frame)



            if Values.SEND_IMAGES_WIFI:
                imageStream.send_image(frame)

            brk = cv2.waitKey(3) & 0xFF
            if brk == ord('q') or brk == 27:
                break
    except ValueError:
        print("Some error accured")
    finally:
        camera.close()
        imageWindow.close()