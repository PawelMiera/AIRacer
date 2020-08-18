from detector.detector import Detector
from settings.settings import Values
from camera.camera import Camera
from PID.PID import PID
import cv2


if __name__ == '__main__':
    detector = Detector(Values.MODEL_PATH, Values.LABEL_PATH)
    camera = Camera()
    pitchPID = PID(0.5, 1000, 2000, 1, 2, 3)
    #rollPID = PID(4, 5, 6)
    #yawPID = PID(7, 8, 9)

    try:
        while True:
            points = detector.detect(camera.get_frame())

    except ValueError:
        print("Some error accured")
