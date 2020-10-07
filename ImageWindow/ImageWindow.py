import cv2
import sys
import os

from PyQt5.QtCore import QTimer, QPoint, pyqtSlot
from PyQt5.QtGui import QFont, QPainter, QImage
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QGridLayout, QPushButton

from settings.settings import Values


class ImageWidget(QWidget):
    def __init__(self, parent=None):
        super(ImageWidget, self).__init__(parent)
        self.image = None

    def setImage(self, image):
        self.image = image
        self.setMinimumSize(image.size())
        self.update()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        if self.image:
            qp.drawImage(QPoint(0, 0), self.image)
        qp.end()


class ImageWindow(QMainWindow):

    def __init__(self, detector):
        super().__init__()
        self.detector = detector
        self.central_widget = QWidget(self)
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
        self.displays = QVBoxLayout()

        self.layout.addWidget(self.yaw_ppm_label, 0, 1)
        self.layout.addWidget(self.roll_ppm_label, 0, 2)
        self.layout.addWidget(self.throttle_ppm_label, 0, 3)

        self.layout.addWidget(P_label, 2, 0)
        self.layout.addWidget(I_label, 3, 0)
        self.layout.addWidget(D_label, 4, 0)
        self.disp = ImageWidget(self)

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

        self.displays.addWidget(self.disp)

        self.displays.addLayout(self.layout)

        self.central_widget.setLayout(self.displays)
        self.setCentralWidget(self.central_widget)

        self.pids = None

    @pyqtSlot()
    def on_click_update(self):
        lines = []
        lines.append(self.yaw_P.text() + ',' + self.roll_P.text() + ',' + self.throttle_P.text() + '\n')
        lines.append(self.yaw_I.text() + ',' + self.roll_I.text() + ',' + self.throttle_I.text() + '\n')
        lines.append(self.yaw_D.text() + ',' + self.roll_D.text() + ',' + self.throttle_D.text() + '\n')
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
        self.pid_start()

    @pyqtSlot()
    def on_click_stop(self):
        self.pid_stop()

    def pid_start(self):
        if self.pids is not None:
            self.pids.update_ppm = True
            self.pids.update_pids = True

    def pid_stop(self):
        if self.pids is not None:
            self.pids.update_ppm = False
            self.pids.update_pids = False

    def start(self):
        self.timer = QTimer(self)  # Timer to trigger display
        self.timer.timeout.connect(lambda: self.show_image(self.detector.frame, self.disp))
        self.timer.start(Values.GUI_UPDATE_MS)

    # Fetch camera image from queue, and display it
    def show_image(self, image, display):
        if image is not None:
            img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            disp_size = img.shape[1], img.shape[0]
            disp_bpl = disp_size[0] * 3
            img = cv2.resize(img, disp_size, interpolation=cv2.INTER_CUBIC)
            qimg = QImage(img.data, disp_size[0], disp_size[1], disp_bpl, QImage.Format_RGB888)
            display.setImage(qimg)

    def flush(self):
        pass

    def closeEvent(self, event):
        self.pids.stop()

    def update_ppm_values(self, yaw, roll, throttle):
        self.throttle_ppm_label.setText(str(round(throttle, 1)))
        self.yaw_ppm_label.setText(str(round(yaw, 1)))
        self.roll_ppm_label.setText(str(round(roll, 1)))

    def keyPressEvent(self, event):
        if event.key() == 16777220:
            self.start()
        if event.key() == 16777216:
            self.stop()

    def get_pids_object(self, my_pids):
        self.pids = my_pids

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

class remoteImageWindow(QMainWindow):
    def __init__(self, tcp_server):
        self.app = QApplication(sys.argv)
        super().__init__()
        self.tcp_server = tcp_server
        self.central_widget = QWidget()
        self.setWindowTitle("AI Racer")

        P_label = QLabel("P")
        I_label = QLabel("I")
        D_label = QLabel("D")

        values = self.get_pid_values()
        self.yaw = QLabel("Yaw")
        self.yaw_ppm_label = QLabel("1500")
        self.yaw_P = QLineEdit(values[0][0])
        self.yaw_I = QLineEdit(values[1][0])
        self.yaw_D = QLineEdit(values[2][0])

        self.roll_ppm_label = QLabel("1500")
        self.roll = QLabel("Roll")
        self.roll_P = QLineEdit(values[0][1])
        self.roll_I = QLineEdit(values[1][1])
        self.roll_D = QLineEdit(values[2][1])

        self.throttle_ppm_label = QLabel("1000")
        self.throttle = QLabel("Throttle")
        self.throttle_P = QLineEdit(values[0][2])
        self.throttle_I = QLineEdit(values[1][2])
        self.throttle_D = QLineEdit(values[2][2])

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
        cv2.waitKey(1)


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
            output_str = "p"
        for line in lines:
            output_str += line
        self.tcp_server.socket.send(output_str.encode())

    @pyqtSlot()
    def on_click_start(self):
        self.start()

    @pyqtSlot()
    def on_click_stop(self):
        self.stop()

    def start(self):
        self.tcp_server.socket.send("s".encode())

    def stop(self):
        self.tcp_server.socket.send("x".encode())

    def update_ppm_values(self, yaw, roll, throttle):
        if yaw is not None:
            self.yaw_ppm_label.setText(yaw)
        elif throttle is not None:
            self.throttle_ppm_label.setText(throttle)
        elif roll is not None:
            self.roll_ppm_label.setText(roll)

    def keyPressEvent(self, event):
        if event.key() == 16777220:
            self.start()
        if event.key() == 16777216:
            self.stop()

    def get_pid_values(self):
        values = []
        with open(os.path.join("settings", "pidValues_remote.csv"), 'r') as fd:
            reader = csv.reader(fd)
            for row in reader:
                values.append(row)
        return values

    def close(self):
        sys.exit(self.app.exec_())