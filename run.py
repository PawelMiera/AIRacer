import sys
from PyQt5.QtWidgets import QApplication
from detector.detector import Detector
from settings.settings import Values
from camera.camera import Camera2
import cv2, threading
import time

if __name__ == '__main__':
    detector = Detector(Values.MODEL_PATH, Values.LABEL_PATH)
    camera = Camera2()
    camera.start()
    pids = None
    
    def main_loop(pids):
        if Values.REMOTE_CONTROL:
            from TCPclient.TCPclient import TCPclient
            from PIDs.PIDs import remotePIDs

            pids = remotePIDs()
            tcpThread = TCPclient(pids)
            tcpThread.start()
            
        if Values.SEND_IMAGES_WIFI:
            from imageStream.imageStream import ImageStream
            imageStream = ImageStream()
        try:
            while True:
                if camera.frame is None:
                    continue
                mid, ratio = detector.detect(camera.frame)         # mid liczony od: lewy gorny rog

                pids.update(mid, ratio)
                
                if not pids.is_running:
                    break
                if Values.SEND_IMAGES_WIFI:
                    imageStream.send_image(cv2.resize(camera.frame, (200, 200)))
                print("OK")
        except ValueError:
            print("Some error accured")
        finally:
            print("Closing")
            camera.close()
            pids.stop()
    if not Values.REMOTE_CONTROL:
        from ImageWindow.ImageWindow import ImageWindow
        from PIDs.PIDs import PIDs
        app = QApplication(sys.argv)
        imageWindow = ImageWindow(detector)
        pids = PIDs(imageWindow)
        time.sleep(1)
        
    t1 = threading.Thread(target=main_loop, args=[pids])
    t1.start()
    
    if not Values.REMOTE_CONTROL:
        imageWindow.show()
        imageWindow.start()
        sys.exit(app.exec_())



  
            
