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
        self.pid_values_changed = True

    @pyqtSlot()
    def on_click_start(self):
        print("click1")

    @pyqtSlot()
    def on_click_stop(self):
        print("click2")

    def update_ppm_values(self, yaw, roll, throttle):
        self.throttle_ppm_label.setText(str(round(throttle, 1)))
        self.yaw_ppm_label.setText(str(round(yaw, 1)))
        self.roll_ppm_label.setText(str(round(roll, 1)))

    def show_pid_values(self, yaw_P, yaw_I, yaw_D, roll_P, roll_I, roll_D, throttle_P, throttle_I, throttle_D):
        self.yaw_P.setText(str(yaw_P))
        self.yaw_I.setText(str(yaw_I))
        self.yaw_D.setText(str(yaw_D))
        self.roll_P.setText(str(roll_P))
        self.roll_I.setText(str(roll_I))
        self.roll_D.setText(str(roll_D))
        self.throttle_P.setText(str(throttle_P))
        self.throttle_I.setText(str(throttle_I))
        self.throttle_D.setText(str(throttle_D))

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



