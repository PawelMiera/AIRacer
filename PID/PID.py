from threading import Timer
from settings.settings import PID_Settings
import time

class PID:
    def __init__(self, set_point, pid_min, pid_max, Kp, Ki, Kd):
        self._timer = None
        self.dt = PID_Settings.PID_REPEAT_TIME
        self.is_running = False
        self.start()
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.set_point = set_point
        self.time = time.time()
        self.max = pid_max
        self.min = pid_min
        self.last_e = None
        self.sum_e = 0
        self.value = None
        self.output = None

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.dt, self._run)
            self._timer.start()
            self.is_running = True

    def _run(self):
        self.is_running = False
        self.start()
        self.calculate()

    def stop(self):
        self._timer.cancel()
        self.is_running = False

    def update(self, v):
        self.value = v

    def calculate(self):
        if self.value is not None:
            e = self.setpoint - self.value

            if self.last_e is not None:
                D = self.Kd * (e - self.last_e) / self.dt
            else:
                D = 0

            self.sum_e += (e * self.dt)

            if self.sum_e > PID_Settings.PID_I_MAX:
                self.sum_e = PID_Settings.PID_I_MAX
            if self.sum_e < - PID_Settings.PID_I_MAX:
                self.sum_e = - PID_Settings.PID_I_MAX

            I = self.Ki * self.sum_e

            #self.output = self.Kp * (e + D + I)
            self.output = self.Kp * e + D + I
            self.last_e = e
        else:
            self.output = 0
