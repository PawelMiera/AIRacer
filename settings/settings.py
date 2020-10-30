import os


class Values:

    MODEL_PATH = os.path.join('models', 'AIRacer_edgetpu.tflite')
    LABEL_PATH = os.path.join('models', 'labelmap.txt')
    DETECTION_THRESHOLD = 0.61

    USE_EDGE_TPU = True
    PRINT_FPS = True
    SEND_IMAGES_WIFI = False
    SENT_IMAGES_SIZE = (200, 200)
    WINDOWS_GPU = False

    REMOTE_CONTROL = False

    WRITE_TO_FILE = False

    CAMERA = 0
    CAMERA_WIDTH = 720
    CAMERA_HEIGHT = 480
    FPS = 122

    PPM_PIN = 12

    REMOTE_IP = "192.168.31.15"
    TCP_PORT = 6969
    IMAGE_STREAM_PORT = 5555
    
    GUI_UPDATE_MS = 50


class PIDSettings:
    PID_PPM_UPDATE_TIME = 1
    PID_I_MAX = 500

    # used in detector to set default values
    THROTTLE_SETPOINT = 0

    ROLL_SETPOINT = 0

    YAW_SETPOINT = 0


class Constants:
    RD = 3
    RU = 0
    LD = 4
    LU = 1
    GATE = 2
