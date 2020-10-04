import cv2
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QVBoxLayout, QApplication, QLabel, QLineEdit, QGridLayout
import os


class ImageWindow(QMainWindow):
    def __init__(self):
        self.app = QApplication([])
        super().__init__()
        self.central_widget = QWidget()
        self.setWindowTitle("AI Racer")

        P_label = QLabel("P")
        I_label = QLabel("I")
        D_label = QLabel("D")

        self.yaw = QLabel("Yaw")
        self.yaw_ppm_label = QLabel("ppm")
        self.yaw_P = QLineEdit("0")
        self.yaw_I = QLineEdit("1")
        self.yaw_D = QLineEdit("2")

        self.roll_ppm_label = QLabel("ppm")
        self.roll = QLabel("Roll")
        self.roll_P = QLineEdit("3")
        self.roll_I = QLineEdit("4")
        self.roll_D = QLineEdit("5")

        self.throttle_ppm_label = QLabel("ppm")
        self.throttle = QLabel("Throttle")
        self.throttle_P = QLineEdit("6")
        self.throttle_I = QLineEdit("7")
        self.throttle_D = QLineEdit("8")

        self.layout = QGridLayout()
        self.layout1 = QVBoxLayout()

        self.layout.addWidget(self.yaw_ppm_label, 0, 1)
        self.layout.addWidget(self.roll_ppm_label, 0, 2)
        self.layout.addWidget(self.throttle_ppm_label, 0, 3)

        self.layout.addWidget(P_label, 2, 0)
        self.layout.addWidget(I_label, 3, 0)
        self.layout.addWidget(D_label, 4, 0)

        self.layout.addWidget(self.yaw, 1, 1)
        self.layout.addWidget(self.yaw_P, 2, 1)
        self.layout.addWidget(self.yaw_I, 3, 1)
        self.layout.addWidget(self.yaw_D, 4, 1)

        self.layout.addWidget(self.roll, 1, 2)
        self.layout.addWidget(self.roll_P, 2, 2)
        self.layout.addWidget(self.roll_I, 3, 2)
        self.layout.addWidget(self.roll_D, 4, 2)

        self.layout.addWidget(self.throttle, 1, 3)
        self.layout.addWidget(self.throttle_P, 2, 3)
        self.layout.addWidget(self.throttle_I, 3, 3)
        self.layout.addWidget(self.throttle_D, 4, 3)

        self.update_button = QPushButton("Update PID")
        self.update_button.clicked.connect(self.on_click_update)
        self.layout.addWidget(self.update_button, 5, 1)

        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.on_click_start)
        self.layout.addWidget(self.start_button, 5, 2)

        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.on_click_stop)
        self.layout.addWidget(self.stop_button, 5, 3)

        self.layout1.addLayout(self.layout)

        self.image_frame = QLabel()
        self.layout1.addWidget(self.image_frame)

        self.central_widget.setLayout(self.layout1)

        self.setCentralWidget(self.central_widget)
        self.update_image(cv2.imread("images/start.jpg"))
        self.pid_values_changed = False
        self.pids = None

    def update_image(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        my_frame = QImage(frame.data, frame.shape[1], frame.shape[0],
                            QImage.Format_RGB888)
        self.image_frame.setPixmap(QPixmap.fromImage(my_frame))

    @pyqtSlot()
    def on_click_update(self):
        lines = []
        lines.append(self.yaw_P.text()+','+self.roll_P.text()+','+self.throttle_P.text()+'\n')
        lines.append(self.yaw_I.text()+','+self.roll_I.text()+','+self.throttle_I.text()+'\n')
        lines.append(self.yaw_D.text()+','+self.roll_D.text()+','+self.throttle_D.text()+'\n')
        with open(os.path.join("settings", "pidValues.csv"), 'w') as fd:
            fd.writelines(lines)
        if self.pids is not None:
            self.pids.yawPID.Kp = float(self.yaw_P.text())
            self.pids.yawPID.Ki = float(self.yaw_I.text())
            self.pids.yawPID.Kd = float(self.yaw_D.text())
            self.pids.rollPID.Kd = float(self.roll_P.text())
            self.pids.rollPID.Ki = float(self.roll_I.text())
            self.pids.rollPID.Kd = float(self.roll_D.text())
            self.pids.throttlePID.Kp = float(self.roll_P.text())
            self.pids.throttlePID.Ki = float(self.roll_I.text())
            self.pids.throttlePID.Kd = float(self.roll_D.text())

    @pyqtSlot()
    def on_click_start(self):
        self.start()

    @pyqtSlot()
    def on_click_stop(self):
        self.stop()

    def start(self):
        if self.pids is not None:
            self.pids.update_ppm = True
            self.pids.update_pids = True

    def stop(self):
        if self.pids is not None:
            self.pids.update_ppm = False
            self.pids.update_pids = False

    def update_ppm_values(self, yaw, roll, throttle):
        self.throttle_ppm_label.setText(str(round(throttle, 1)))
        self.yaw_ppm_label.setText(str(round(yaw, 1)))
        self.roll_ppm_label.setText(str(round(roll, 1)))

    def keyPressEvent(self, event):
        if event.key() == 16777220:
            self.start()
        if event.key() == 16777216:
            self.stop()

    def show_pid_values(self):
        if self.pids is not None:
            self.yaw_P.setText(str(self.pids.yawPID.Kp))
            self.yaw_I.setText(str(self.pids.yawPID.Ki))
            self.yaw_D.setText(str(self.pids.yawPID.Kd))
            self.roll_P.setText(str(self.pids.rollPID.Kp))
            self.roll_I.setText(str(self.pids.rollPID.Ki))
            self.roll_D.setText(str(self.pids.rollPID.Kd))
            self.throttle_P.setText(str(self.pids.throttlePID.Kp))
            self.throttle_I.setText(str(self.pids.throttlePID.Ki))
            self.throttle_D.setText(str(self.pids.throttlePID.Kd))

    def get_pids_object(self, my_pids):
        self.pids = my_pids

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



