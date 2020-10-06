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
imageWindow.show()


def handle_receive():
    try:
        print("Started TCP server!")
        while 1:
            newSocket, address = tcp_server.sock.accept()
            tcp_server.socket = newSocket
            while 1:
                try:
                    receivedData = newSocket.recv(1024).decode()  # receive data from server
                    if receivedData[0] == "t":
                        imageWindow.update_ppm_values(None, None, receivedData[1:])
                    elif receivedData[0] == "y":
                        imageWindow.update_ppm_values(receivedData[1:], None, None)
                    elif receivedData[0] == "r":
                        imageWindow.update_ppm_values(None, receivedData[1:], None)
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
        received_string = footage_socket.recv_string()
        img = base64.b64decode(received_string)
        npimg = np.frombuffer(img, dtype=np.uint8)
        frame = cv2.imdecode(npimg, 1)
        imageWindow.update_image(frame)
        cv2.waitKey(1)
        if time.time() - start > 1:
            start = time.time()
            print("FPS " + str(ind))
            ind = 0

    except KeyboardInterrupt:
        cv2.destroyAllWindows()
        break