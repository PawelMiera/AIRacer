import os


class Values:

    MODEL_PATH = os.path.join('models', 'AIRacer_FPV_edgetpu.tflite')

    DETECTION_THRESHOLD = 0.499  #0.61

    USE_EDGE_TPU = True
    PRINT_FPS = True
    SEND_IMAGES_WIFI = False
    SENT_IMAGES_SIZE = (200, 200)
    WINDOWS_GPU = False

    REMOTE_CONTROL = False

    WRITE_TO_FILE = False

    WINDOWS_TESTS = False

    CAMERA = 0
    CAMERA_WIDTH = 640
    CAMERA_HEIGHT = 480
    FPS = 122

    PPM_PIN = 21

    REMOTE_IP = "192.168.31.15"
    TCP_PORT = 6969
    IMAGE_STREAM_PORT = 5555
    
    GUI_UPDATE_MS = 50


class PIDSettings:
    PID_PPM_UPDATE_TIME = 0.03

    PID_I_MAX = 400

    # used in detector to set default values
    THROTTLE_SETPOINT = 0

    ROLL_SETPOINT = 0

    YAW_SETPOINT = 0


class Constants:
    RD = 4
    RU = 1
    LD = 3
    LU = 0
    GATE = 2
