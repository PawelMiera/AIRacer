from PID.PID import PID
from settings.settings import PIDSettings as ps
#from PPM.PPM import PPM
from ImageWindow.ImageWindow import ImageWindow
from threading import Timer
import csv
import os


class PIDs:
    def __init__(self, imWindow:ImageWindow):
        self.imageWindow = imWindow
        self._timer = None
        self.dt = ps.PID_PPM_UPDATE_TIME
        self.is_running = False
        #self.ppm = PPM()
        self.update_ppm = False
        self.update_pids = False
        values = self.get_pid_values()
        self.yawPID = PID(ps.YAW_SETPOINT, 1000, 2000, float(values[0][0]), float(values[1][0]), float(values[2][0]))
        self.rollPID = PID(ps.ROLL_SETPOINT, 1000, 2000, float(values[0][1]), float(values[1][1]), float(values[2][1]))
        self.throttlePID = PID(ps.THROTTLE_SETPOINT, 1000, 2000, float(values[0][2]), float(values[1][2]), float(values[2][2]), start_from_min=True)
        #pitchPID = PID(0.5, 1000, 2000, 1, 2, 3)
        self.imageWindow.get_pids_object(self)
        self.imageWindow.show_pid_values()
        self.start()

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.dt, self._run)
            self._timer.start()
            self.is_running = True

    def _run(self):
        self.is_running = False
        self.start()
        self.calculate_pids()
        self.send_ppm()
        self.imageWindow.update_ppm_values(self.yawPID.output_ppm, self.rollPID.output_ppm, self.throttlePID.output_ppm)

    def stop(self):
        self._timer.cancel()
        self.is_running = False

    def send_ppm(self):
        if self.update_ppm:
            print(self.yawPID.output_ppm, self.rollPID.output_ppm, self.throttlePID.output_ppm,
                  self.yawPID.value, self.rollPID.value, self.throttlePID.value)
        else:
            print("all ppm to lowest value")

    def calculate_pids(self):
        if self.update_pids:
            self.yawPID.calculate()
            self.throttlePID.calculate()
            self.rollPID.calculate()
        else:
            self.yawPID.reset()
            self.rollPID.reset()
            self.throttlePID.reset()

    def update(self, mid, ratio):
        in_min = 0
        in_max = 1
        out_max = 1
        out_min = -1
        mid[0] = (mid[0] - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
        mid[1] = -((mid[1] - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)
        self.yawPID.update(ratio)
        self.rollPID.update(mid[0])
        self.throttlePID.update(-mid[1])

    def get_pid_values(self):
        values = []
        with open(os.path.join("settings", "pidValues.csv"), 'r') as fd:
            reader = csv.reader(fd)
            for row in reader:
                values.append(row)
        return values

    def update_P_I_D_values(self):
        values = self.get_pid_values()

        self.yawPID.Kp = float(values[0][0])
        self.yawPID.Ki = float(values[1][0])
        self.yawPID.Kd = float(values[2][0])

        self.rollPID.Kp = float(values[0][1])
        self.rollPID.Ki = float(values[1][1])
        self.rollPID.Kd = float(values[2][1])

        self.throttlePID.Kp = float(values[0][2])
        self.throttlePID.Ki = float(values[1][2])
        self.throttlePID.Kd = float(values[2][2])


class remotePIDs:
    def __init__(self):
        self._timer = None
        self.dt = ps.PID_PPM_UPDATE_TIME
        self.is_running = False
        #self.ppm = PPM()
        self.update_ppm = False
        self.update_pids = False
        values = self.get_pid_values()

        self.yawPID = PID(ps.YAW_SETPOINT, 1000, 2000, float(values[0][0]), float(values[1][0]), float(values[2][0]))
        self.rollPID = PID(ps.ROLL_SETPOINT, 1000, 2000, float(values[0][1]), float(values[1][1]), float(values[2][1]))
        self.throttlePID = PID(ps.THROTTLE_SETPOINT, 1000, 2000, float(values[0][2]), float(values[1][2]), float(values[2][2]), start_from_min=True)
        #pitchPID = PID(0.5, 1000, 2000, 1, 2, 3)

        self.start()

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.dt, self._run)
            self._timer.start()
            self.is_running = True

    def _run(self):
        self.is_running = False
        self.start()
        self.calculate_pids()
        self.send_ppm()

    def stop(self):
        self._timer.cancel()
        self.is_running = False

    def send_ppm(self):
        if self.update_ppm:
            print(self.yawPID.output_ppm, self.rollPID.output_ppm, self.throttlePID.output_ppm,
                  self.yawPID.value, self.rollPID.value, self.throttlePID.value)
        else:
            print("all ppm to lowest value")

    def calculate_pids(self):
        if self.update_pids:
            self.yawPID.calculate()
            self.throttlePID.calculate()
            self.rollPID.calculate()
        else:
            self.yawPID.reset()
            self.rollPID.reset()
            self.throttlePID.reset()

    def update(self, mid, ratio):
        in_min = 0
        in_max = 1
        out_max = 1
        out_min = -1
        mid[0] = (mid[0] - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
        mid[1] = -((mid[1] - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)
        self.yawPID.update(ratio)
        self.rollPID.update(mid[0])
        self.throttlePID.update(-mid[1])

    def get_pid_values(self):
        values = []
        with open(os.path.join("settings", "pidValues.csv"), 'r') as fd:
            reader = csv.reader(fd)
            for row in reader:
                values.append(row)
        return values

    def update_P_I_D_values(self):
        values = self.get_pid_values()

        self.yawPID.Kp = float(values[0][0])
        self.yawPID.Ki = float(values[1][0])
        self.yawPID.Kd = float(values[2][0])

        self.rollPID.Kp = float(values[0][1])
        self.rollPID.Ki = float(values[1][1])
        self.rollPID.Kd = float(values[2][1])

        self.throttlePID.Kp = float(values[0][2])
        self.throttlePID.Ki = float(values[1][2])
        self.throttlePID.Kd = float(values[2][2])
