import cv2
from PIDs.PIDs import PIDs
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QVBoxLayout, QApplication, QLabel, QLineEdit, QGridLayout
import os

class ImageWindow(QMainWindow):
    def __init__(self, pids: PIDs):
        self.pids = pids
        self.app = QApplication([])
        super().__init__()
        self.central_widget = QWidget()
        self.setWindowTitle("AI Racer")

        P_label = QLabel("P")
        I_label = QLabel("I")
        D_label = QLabel("D")

        self.yaw = QLabel("Yaw")
        self.yaw_P = QLineEdit(str(self.pids.yawPID.Kp))
        self.yaw_I = QLineEdit(str(self.pids.yawPID.Ki))
        self.yaw_D = QLineEdit(str(self.pids.yawPID.Kd))

        self.roll = QLabel("Roll")
        self.roll_P = QLineEdit(str(self.pids.rollPID.Kp))
        self.roll_I = QLineEdit(str(self.pids.rollPID.Ki))
        self.roll_D = QLineEdit(str(self.pids.rollPID.Kd))

        self.throttle = QLabel("Throttle")
        self.throttle_P = QLineEdit(str(self.pids.throttlePID.Kp))
        self.throttle_I = QLineEdit(str(self.pids.throttlePID.Ki))
        self.throttle_D = QLineEdit(str(self.pids.throttlePID.Kd))

        self.layout = QGridLayout()
        self.layout1 = QVBoxLayout()

        self.layout.addWidget(P_label, 1, 0)
        self.layout.addWidget(I_label, 2, 0)
        self.layout.addWidget(D_label, 3, 0)

        self.layout.addWidget(self.yaw, 0, 1)
        self.layout.addWidget(self.yaw_P, 1, 1)
        self.layout.addWidget(self.yaw_I, 2, 1)
        self.layout.addWidget(self.yaw_D, 3, 1)
        self.layout.addWidget(self.roll, 0, 2)
        self.layout.addWidget(self.roll_P, 1, 2)
        self.layout.addWidget(self.roll_I, 2, 2)
        self.layout.addWidget(self.roll_D, 3, 2)
        self.layout.addWidget(self.throttle, 0, 3)
        self.layout.addWidget(self.throttle_P, 1, 3)
        self.layout.addWidget(self.throttle_I, 2, 3)
        self.layout.addWidget(self.throttle_D, 3, 3)

        self.update_button = QPushButton("Update PID")
        self.update_button.clicked.connect(self.on_click_update)
        self.layout.addWidget(self.update_button, 4, 1)

        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.on_click_start)
        self.layout.addWidget(self.start_button, 4, 2)

        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.on_click_stop)
        self.layout.addWidget(self.stop_button, 4, 3)

        self.layout1.addLayout(self.layout)

        self.image_frame = QLabel()
        self.layout1.addWidget(self.image_frame)

        self.central_widget.setLayout(self.layout1)

        self.setCentralWidget(self.central_widget)
        self.update_image(cv2.imread("images/start.jpg"))

    def update_image(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        my_frame = QImage(frame.data, frame.shape[1], frame.shape[0],
                            QImage.Format_RGB888)
        self.image_frame.setPixmap(QPixmap.fromImage(my_frame))

    @pyqtSlot()
    def on_click_update(self):
        lines = []
        lines.append(self.yaw_P.text()+','+self.yaw_I.text()+','+self.yaw_D.text()+'\n')
        lines.append(self.roll_P.text()+','+self.roll_I.text()+','+self.roll_D.text()+'\n')
        lines.append(self.throttle_P.text()+','+self.throttle_I.text()+','+self.throttle_D.text()+'\n')
        with open(os.path.join("settings", "pidValues.csv"), 'w') as fd:
            fd.writelines(lines)

    @pyqtSlot()
    def on_click_start(self):
        print("click1")

    @pyqtSlot()
    def on_click_stop(self):
        print("click2")

    def close(self):
        self.app.exit(self.app.exec_())
if __name__ == '__main__':

    window = ImageWindow()
    window.show()

    camera = cv2.VideoCapture(0)
    while True:
        ret, frame = camera.read()
        window.update_image(frame)
        cv2.waitKey(1)

    window.close()



