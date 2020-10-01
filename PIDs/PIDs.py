from PID.PID import PID
from settings.settings import PIDSettings as ps
import csv
import os


class PIDs:
    def __init__(self):
        self.update_pids = False
        values = []
        with open(os.path.join("settings", "pidValues.csv"), 'r') as fd:
            reader = csv.reader(fd)
            for row in reader:
                values.append(row)
        #pitchPID = PID(0.5, 1000, 2000, 1, 2, 3)
        self.yawPID = PID(ps.YAW_SETPOINT, 1000, 2000, float(values[0][0]), float(values[0][1]), float(values[0][2]))
        self.rollPID = PID(ps.ROLL_SETPOINT, 1000, 2000, float(values[1][0]), float(values[1][1]),float(values[1][2]))
        self.throttlePID = PID(ps.THROTTLE_SETPOINT, 1000, 2000, float(values[2][0]), float(values[2][1]), float(values[2][2]), start_from_min=True)

    def update(self, mid, ratio):
        if self.update_pids:
            in_min = 0
            in_max = 1
            out_max = 1
            out_min = -1
            mid[0] = (mid[0] - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
            mid[1] = -((mid[1] - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)
            self.yawPID.update(ratio)
            self.rollPID.update(mid[0])
            self.throttlePID.update(mid[1])
        else:
            self.rollPID.stop()
            self.yawPID.stop()
            self.throttlePID.stop()
            self.throttlePID.output_ppm = 1000
