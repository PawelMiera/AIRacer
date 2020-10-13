from threading import Thread
import cv2
from settings.settings import Values
import time


class Camera2:
    def __init__(self):
        self.camera = cv2.VideoCapture(Values.CAMERA, cv2.CAP_DSHOW)
        #self.camera.set(3, Values.CAMERA_WIDTH)
        #self.camera.set(4, Values.CAMERA_HEIGHT)
        if Values.PRINT_FPS:
            self.count = 0
            self.start = time.time()

    def get_frame(self):
        ret, frame = self.camera.read()
        if Values.PRINT_FPS:
            self.count += 1
            if time.time() - self.start > 1:
                self.start = time.time()
                print("FPS: " + str(self.count))
                self.count = 0

        if ret:
            return frame
        else:
            return False
    def close(self):
        self.camera.release()
        cv2.destroyAllWindows()


class Camera(Thread):
    def __init__(self):
        Thread.__init__(self)
        #self.camera = cv2.VideoCapture(Values.CAMERA)
        self.frame = None
        self.stop = False

    def run(self):
        while True:
            if self.stop:
                break
            self.frame = cv2.imread("images/start.jpg")
            #ret, self.frame = self.camera.read()
            #self.frame = cv2.imread("images/start.jpg")
            cv2.waitKey(10)
    def close(self):
        self.stop = True