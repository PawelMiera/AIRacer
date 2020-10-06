from detector.detector import Detector
from settings.settings import Values
from camera.camera import Camera
import cv2
import time


if __name__ == '__main__':
    detector = Detector(Values.MODEL_PATH, Values.LABEL_PATH)
    camera = Camera()

    if Values.REMOTE_CONTROL:
        from TCPclient.TCPclient import TCPclient
        from PIDs.PIDs import remotePIDs

        pids = remotePIDs()
        tcpThread = TCPclient(pids)
        tcpThread.start()
    else:
        from ImageWindow.ImageWindow import ImageWindow
        from PIDs.PIDs import PIDs

        imageWindow = ImageWindow()
        imageWindow.show()
        pids = PIDs(imageWindow)       #pewnie beda zle wartosci na wyjsciu do dopracowania

    if Values.SEND_IMAGES_WIFI:
        from imageStream.imageStream import ImageStream
        imageStream = ImageStream()

    i = 0
    try:
        while True:
            i += 1
            name = "images/" + str(i) + ".JPG"
            #frame = cv2.imread(name)
            #frame = cv2.resize(frame, (640, 480))
            frame = camera.get_frame()
            if frame is None:
                continue
            mid, ratio = detector.detect(frame)         # mid liczony od: lewy gorny rog

            pids.update(mid, ratio)

            if not Values.REMOTE_CONTROL:
                imageWindow.update_image(frame)

            if Values.SEND_IMAGES_WIFI:
                imageStream.send_image(cv2.resize(frame, (200, 200)))

            brk = cv2.waitKey(1) & 0xFF
            if brk == ord('q') or brk == 27:
                print("break")
                break
    except ValueError:
        print("Some error accured")
    finally:
        print("Closing")
        camera.close()
        if not Values.REMOTE_CONTROL:
            imageWindow.close()
        pids.stop()