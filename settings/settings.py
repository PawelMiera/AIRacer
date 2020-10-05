import os


class Values:

    MODEL_PATH = os.path.join('models', 'AIRacer.tflite')
    LABEL_PATH = os.path.join('models', 'labelmap.txt')
    DETECTION_THRESHOLD = 0.61

    USE_EDGE_TPU = False
    SHOW_IMAGES = False
    PRINT_FPS = True
    SEND_IMAGES_WIFI = False
    WINDOWS_GPU = False

    REMOTE_CONTROL = True
    CAMERA = 0
    CAMERA_WIDTH = 720
    CAMERA_HEIGHT = 480
    STREAM_PORT = 5555
    FPS = 122

    PPM_PIN = 4

    TCP_IP = "localhost"
    TCP_PORT = 500


class PIDSettings:
    PID_PPM_UPDATE_TIME = 1
    PID_I_MAX = 500

    # used in detector to set default values
    THROTTLE_SETPOINT = 0
    THROTTLE_P = 1
    THROTTLE_I = 1
    THROTTLE_D = 1

    ROLL_SETPOINT = 0
    ROLL_P = 1
    ROLL_I = 1
    ROLL_D = 1

    YAW_SETPOINT = 0
    YAW_P = 1
    YAW_I = 1
    YAW_D = 1


class Constants:
    RD = 3
    RU = 0
    LD = 4
    LU = 1
    GATE = 2
