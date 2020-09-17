import os


class Modes:
    DETECTOR = 0
    CLASSIFIER = 1


class Values:
    MODE = Modes.DETECTOR
    MODEL_PATH = os.path.join('models', 'AIRacer.tflite')
    LABEL_PATH = os.path.join('models', 'labelmap.txt')
    DETECTION_THRESHOLD = 0.61

    USE_EDGE_TPU = False
    SHOW_IMAGES = False
    PRINT_FPS = True
    SEND_IMAGES_WIFI = False
    CAMERA = 0
    CAMERA_WIDTH = 640
    CAMERA_HEIGHT = 480
    STREAM_PORT = 5555
    FPS = 122


class PIDSettings:
    PID_REPEAT_TIME = 1
    PID_I_MAX = 500

class Constants:
    RD = 3
    RU = 0
    LD = 4
    LU = 1
    GATE = 2
