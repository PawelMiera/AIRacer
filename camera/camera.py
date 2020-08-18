import cv2
from settings.settings import Values


class Camera:
    def __init__(self):
        self.camera = cv2.VideoCapture(Values.CAMERA)
        self.camera.set(3, Values.CAMERA_WIDTH)
        self.camera.set(4, Values.CAMERA_HEIGHT)

    def get_frame(self):
        ret, frame = self.camera.read()
        if ret:
            return frame
        else:
            return False
