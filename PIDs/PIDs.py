from PID.PID import PID
from settings.settings import PIDSettings as ps
from settings.settings import Values
if not Values.WINDOWS_TESTS:
    from PPM.PPM import My_PPM
from threading import Timer
import csv
import os
import time


class PIDs:
    def __init__(self):
        self._timer = None
        self.dt = ps.PID_PPM_UPDATE_TIME
        self.is_running = False
        if not Values.WINDOWS_TESTS:            # do wywalenia pozniej bo szkoda obliczen
            self.ppm = My_PPM()
        self.update_ppm = False
        self.update_pids = False
        self.first_start = True
        self.starting = False
        self.slow_landing = False
        values = self.get_pid_values()
        self.yawPID = PID(ps.YAW_SETPOINT, 1000, 2000, float(values[0][0]), float(values[1][0]), float(values[2][0]))
        self.rollPID = PID(ps.ROLL_SETPOINT, 1000, 2000, float(values[0][1]), float(values[1][1]), float(values[2][1]))
        self.throttlePID = PID(ps.THROTTLE_SETPOINT, 1000, 2000, float(values[0][2]), float(values[1][2]), float(values[2][2]))
        self.pitchPID = PID(ps.PITCH_SETPOINT, 1000, 2000, float(values[0][3]), float(values[1][3]), float(values[2][3]))
        
        self.last_time = time.time()

        self.hold_possition = True

        if Values.WRITE_TO_FILE:
            self.file = open('inputs_outputs.csv', 'a')
        if not Values.WINDOWS_TESTS:
            self.ppm.update_ppm_channels([1500, 1500, 1000, 1500, 1100, 1800, 1000, 1000])
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
        if self.update_ppm and not self.starting:
            self.send_ppm()

        if Values.WRITE_TO_FILE:
            self.write_to_file()

    def slow_land(self):
        if self.slow_landing:        
            print("Stopped slow landing!!")
            self.slow_landing = False
        else:
            print("Started slow landing!!")
            self.slow_landing = True


    def land(self):
        print("Landing!!")
        self.slow_landing = False
        self.update_ppm = False
        self.update_pids = False
        self.first_start = True
        self.hold_possition = True
        self.starting = False
        if not Values.WINDOWS_TESTS:
            self.ppm.update_ppm_channels([1500, 1500, 1000, 1500, 1100, 1800, 1000, 1000])

    def go_for_it(self):
        if self.hold_possition:
            print("Go go!!")
            self.hold_possition = False
        else:
            print("Please don't go!!")
            self.hold_possition = True

    def stop(self):
        print("Closing pids!")
        self._timer.cancel()
        self.is_running = False
        self.update_ppm = False         ################## ??????????? moze cos byc  nie tak
        self.update_pids = False
        self.first_start = True
        if not Values.WINDOWS_TESTS:
            self.ppm.update_ppm_channels([1500, 1500, 1000, 1500, 1100, 1800, 1000, 1000])
        if Values.WRITE_TO_FILE:
            self.file.close()


    def send_ppm(self):

        if not Values.WINDOWS_TESTS:
            if self.first_start:
                print("Starting sequence!!")
                self.first_start = False
                self.starting = True
                self.slow_landing = False
                self.ppm.update_ppm_channels([1500, 1500, 1000, 1500, 1100, 1800, 1000, 1000])
                time.sleep(1)
                self.ppm.update_ppm_channels([1500, 1500, 1000, 1500, 1800, 1800, 1000, 1000])
                time.sleep(1)
                self.ppm.update_ppm_channels([1500, 1500, 1000, 1500, 1800, 1100, 1000, 1000])
                time.sleep(1)
                self.ppm.update_ppm_channels([1500, 1500, 1900, 1500, 1800, 1100, 1000, 1000])
                time.sleep(5)
                self.ppm.update_ppm_channels([1500, 1500, 1500, 1500, 1800, 1100, 1000, 1000])

                self.starting = False
                if Values.WRITE_TO_FILE:
                    self.file.write("start \n")
                print("Started!!")

            pitch = int(self.pitchPID.output_ppm)
            yaw = int(self.yawPID.output_ppm)
            roll = int(self.rollPID.output_ppm)
            throttle = int(self.throttlePID.output_ppm)

            roll_with_yaw = yaw - 1500 + roll

            if roll_with_yaw > 2000:
                roll_with_yaw = 2000
            elif roll_with_yaw < 1000:
                roll_with_yaw = 1000

            if not self.hold_possition:
                pitch = 1600

            throttle = 1900
            
            if self.slow_landing:
                throttle = 1120
                roll_with_yaw = 1500
                pitch = 1500
                roll = 1500

            vals = [roll_with_yaw, pitch, throttle, roll, 1800, 1100, 1000, 1000]
            self.ppm.update_ppm_channels(vals)
        else:
            pitch = int(self.pitchPID.output_ppm)
            yaw = int(self.yawPID.output_ppm)
            roll = int(self.rollPID.output_ppm)
            throttle = int(self.throttlePID.output_ppm)

            roll_with_yaw = yaw - 1500 + roll
            print(roll_with_yaw, roll, yaw)

    def calculate_pids(self):
        if self.update_pids:
            self.yawPID.calculate()
            self.throttlePID.calculate()
            self.rollPID.calculate()
            self.pitchPID.calculate()
        else:
            self.yawPID.reset()
            self.rollPID.reset()
            self.throttlePID.reset()
            self.pitchPID.reset()

    def update(self, mid, ratio, pitch_input):
        in_min = 0
        in_max = 1
        out_max = 1
        out_min = -1
        mid[0] = (mid[0] - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
        mid[1] = -((mid[1] - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)
        if mid[0] < 0:
            ratio *= -1
        self.yawPID.update(-ratio)
        self.rollPID.update(-mid[0])
        self.throttlePID.update(-mid[1])
        self.pitchPID.update(pitch_input)

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

    def write_to_file(self):
        line = str(self.yawPID.value) + "," + str(self.yawPID.output_ppm) + "," + str(self.rollPID.value) + "," + \
              str(self.rollPID.output_ppm) + "," + str(self.throttlePID.value) + "," + \
              str(self.throttlePID.output_ppm) + "," + str(self.pitchPID.value) + "," + str(self.pitchPID.output_ppm) + "\n"
        self.file.write(line)
