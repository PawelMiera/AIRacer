import os


class Values:

    MODEL_PATH = os.path.join('models', 'AIRacer_Real_edgetpu.tflite')

    DETECTION_THRESHOLD = 0.499  #0.61

    USE_EDGE_TPU = True
    PRINT_FPS = False
    SEND_IMAGES_WIFI = False
    SENT_IMAGES_SIZE = (200, 200)

    REMOTE_CONTROL = False

    WRITE_TO_FILE = True

    WINDOWS_TESTS = False

    OUTPUT_LIMIT = False

    OUTPUT_LIMIT_VALUE = 30

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

    PID_I_MAX = 300
    """wszystkie wartości od 0 do 1"""

    THROTTLE_SETPOINT = 0.7                   #### wieksze wyzej leci

    ROLL_SETPOINT = 0                            #### wiecej to bramka bardziej po lewej stronie drona

    YAW_SETPOINT = 0

    PITCH_SETPOINT = 0                    ### wieksze to bliżej bramki

    SIDES_RATIO_INFLUENCE = 0
    MID_INFLUENCE = 1


class Constants:
    RD = 3
    RU = 0
    LD = 4
    LU = 1
    CORNERS = 1
    GATE = 0
