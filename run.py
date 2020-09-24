from detector.detector import Detector
from settings.settings import Values
from camera.camera import Camera
from PID.PID import PID
#from PIDThrottle.PIDThrottle import PIDThrottle
from imageStream.imageStream import ImageStream
import cv2


if __name__ == '__main__':
    detector = Detector(Values.MODEL_PATH, Values.LABEL_PATH)
    camera = Camera()
    if Values.SEND_IMAGES_WIFI:
        imageStream = ImageStream()

    #pitchPID = PID(0.5, 1000, 2000, 1, 2, 3)
    #pitchPID = PID(0.5, 1000, 2000, 1, 2, 3)
    #pitchPID = PID(0.5, 1000, 2000, 1, 2, 3)
    #throttlePID = PID(0.5, 1000, 2000, 7, 8, 9, start_from_min=True)
    i =0
    try:
        while True:
            i +=1
            name = "images/" + str(i)+".JPG"
            frame = cv2.imread(name)
            frame = cv2.resize(frame, (640, 480))
            #frame = camera.get_frame()
            detector.detect(frame)
            cv2.imshow("xd", frame)
            if Values.SEND_IMAGES_WIFI:
                imageStream.send_image(frame)
            cv2.waitKey(0)
            brk = cv2.waitKey(1) & 0xFF
            if brk == ord('q') or brk == 27:
                break
    except ValueError:
        print("Some error accured")
    camera.close()
