import cv2
import zmq
import base64
import numpy as np
import time

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
        cv2.imshow("Stream", source)
        cv2.waitKey(1)
        if time.time() - start > 1:
            start = time.time()
            print("FPS " + str(ind))
            ind = 0

    except KeyboardInterrupt:
        cv2.destroyAllWindows()
        break