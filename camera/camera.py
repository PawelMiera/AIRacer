from threading import Thread
import cv2
from settings.settings import Values
import time


class Camera2:
    def __init__(self):
        self.camera = cv2.VideoCapture(Values.CAMERA)
        #self.camera.set(3, Values.CAMERA_WIDTH)
        #self.camera.set(4, Values.CAMERA_HEIGHT)


    def get_frame(self):
        ret, frame = self.camera.read()
        #cv2.imshow("xd", frame)
        #cv2.waitKey(1)
        if ret:
            return frame
        else:
            return None
    def close(self):
        self.camera.release()
        cv2.destroyAllWindows()


class Camera(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.camera = cv2.VideoCapture(Values.CAMERA)
        self.frame = None
        self.stop = False
        self.new_frame = False

    def run(self):
        while True:
            if self.stop:
                break
            #self.frame = cv2.imread("images/start.jpg")
            ret, self.frame = self.camera.read()
            cv2.imshow("xd", self.frame)
            self.new_frame = True
            cv2.waitKey(1)
        self.camera.release()

    def get_frame(self):
        if self.new_frame:
            self.new_frame = False
            return self.frame
        else:
            return None

    def close(self):
        self.stop = True