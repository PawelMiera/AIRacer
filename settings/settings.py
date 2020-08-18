import os


class Modes:
    DETECTOR = 0
    CLASSIFIER = 1


class Values:
    MODE = Modes.DETECTOR
    MODEL_PATH = os.path.join('models', 'detection.tflite')
    LABEL_PATH = os.path.join('models', 'labelmap.txt')
    DETECTION_THRESHOLD = 0.61

    USE_EDGE_TPU = False
    SHOW_IMAGES = True
    PRINT_FPS = True
    CAMERA = 0
    CAMERA_WIDTH = 640
    CAMERA_HEIGHT = 480
    FPS = 122


class PID_Settings:
    PID_REPEAT_TIME = 1
    PID_I_MAX = 500
