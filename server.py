import base64
import threading
import time

import cv2
import numpy as np
import zmq

from ImageWindow.ImageWindow import remoteImageWindow
from TCPserver.TCPserver import TCPserver
from settings.settings import Values

tcp_server = TCPserver(Values.TCP_PORT)
imageWindow = remoteImageWindow(tcp_server)

def handle_receive():
    try:
        while 1:
            newSocket, address = tcp_server.sock.accept()
            tcp_server.socket = newSocket
            while 1:
                try:
                    print("receiving")
                    receivedData = newSocket.recv(1024)  # receive data from server
                except ConnectionResetError:
                    print("Lost connection!")
            newSocket.close()
    except KeyboardInterrupt:
        tcp_server.sock.close()


t1 = threading.Thread(target=handle_receive)
t1.start()

context = zmq.Context()
footage_socket = context.socket(zmq.SUB)
footage_socket.bind('tcp://127.0.0.1:5555')
footage_socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))



start = time.time()
ind = 0

while True:

    try:
        ind += 1
        frame = footage_socket.recv_string()
        img = base64.b64decode(frame)
        npimg = np.frombuffer(img, dtype=np.uint8)
        source = cv2.imdecode(npimg, 1)
        imageWindow.update_image(source)
        cv2.waitKey(1)
        if time.time() - start > 1:
            start = time.time()
            print("FPS " + str(ind))
            ind = 0

    except KeyboardInterrupt:
        cv2.destroyAllWindows()
        break