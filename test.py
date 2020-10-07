import sys
from PyQt5.QtWidgets import QApplication
from detector.detector import Detector
from settings.settings import Values
from camera.camera import Camera2
import cv2
import time, threading

from ImageWindow.ImageWindow import ImageWindow

camera = Camera2()
camera.start()


def start_gui():
    while True:
        print("xd")
        time.sleep(1)
    

t1 = threading.Thread(target=start_gui)
t1.start()

app = QApplication(sys.argv)
imageWindow = ImageWindow(camera)
imageWindow.show()
imageWindow.start()

    
sys.exit(app.exec_())
