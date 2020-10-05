import threading, socket
from settings.settings import Values
from PIDs.PIDs import PIDs
import time


class TCPclient(threading.Thread):
    def __init__(self, pids:PIDs):
        threading.Thread.__init__(self)
        self.pids = pids
        self.ip = Values.TCP_IP
        self.port = Values.TCP_PORT
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.connect((self.ip, self.port))
        self.last_yaw_output = self.pids.yawPID.output_ppm
        self.last_roll_output = self.pids.rollPID.output_ppm
        self.last_throttle_output = self.pids.throttlePID.output_ppm

    def run(self):
        t1 = threading.Thread(target=self.handle_receive)
        t2 = threading.Thread(target=self.handle_send)
        t1.start()
        t2.start()
        t1.join()
        t2.join()


    def handle_receive(self):
        while True:
            data = self.socket.recv(1024).decode()
            print(data)
            if data == "s":
                self.pids.update_ppm = True
                self.pids.update_pids = True
            elif data == "x":
                self.pids.update_ppm = False
                self.pids.update_pids = False
            elif data[0] == "u":
                print("pid upd")


    def handle_send(self):
        while True:
            if self.pids.yawPID.output_ppm != self.last_yaw_output:
                self.socket.send(("y" + str(round(self.pids.yawPID.output_ppm, 1))).encode())
                self.last_yaw_output = self.pids.yawPID.output_ppm
                time.sleep(0.03)

            if self.pids.rollPID.output_ppm != self.last_roll_output:
                self.socket.send(("r" + str(round(self.pids.rollPID.output_ppm, 1))).encode())
                self.last_roll_output = self.pids.rollPID.output_ppm
                time.sleep(0.03)

            if self.pids.throttlePID.output_ppm != self.last_throttle_output:
                self.socket.send(("t" + str(round(self.pids.throttlePID.output_ppm, 1))).encode())
                self.last_throttle_output = self.pids.throttlePID.output_ppm
                time.sleep(0.03)
            time.sleep(0.05)

    def close(self):
        self.socket.close()


