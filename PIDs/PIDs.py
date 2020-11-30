from PID.PID import PID
from settings.settings import PIDSettings as ps
from settings.settings import Values
from PPM.PPM import My_PPM
from threading import Timer
import csv
import os
import time
import logging
from datetime import datetime


class PIDs:
    def __init__(self):
        self._timer = None
        self.dt = ps.PID_PPM_UPDATE_TIME
        self.is_running = False          # do wywalenia pozniej bo szkoda obliczen
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
        self.gate_lost = False
        self.hold_possition = True
        self.seen_gate_time = 0
        self.finding_mode = 0
        self.last_mode_time = 0
        self.last_variability = 1

        if Values.WRITE_TO_FILE:

            now = datetime.now()
            fname = now.strftime('%Y-%m-%d_%H-%M-%S')
            fname += '.log'
            file_handler = [logging.FileHandler(filename=fname)]
            logging.basicConfig(level=logging.INFO, format='%(message)s', handlers=file_handler)
            #self.file = open('inputs_outputs.csv', 'a')

        self.ppm.update_ppm_channels([1500, 1500, 1000, 1500, 1100, 1800, 1000, 1000])
        self.start()

    def update(self, mid, sides_ratio, pitch_input):

        if pitch_input is None:
            pitch_input = ps.PITCH_SETPOINT

        if sides_ratio is None:
            sides_ratio = 0

        variability = 1

        if mid is None:
            if (time.time() - self.seen_gate_time > 2.5) and not self.first_start:
                if not self.gate_lost:
                    print("Gate lost!")
                    self.finding_mode = 0
                    self.last_mode_time = time.time()
                self.gate_lost = True
            mid = (ps.ROLL_SETPOINT, ps.THROTTLE_SETPOINT)
            variability = self.last_variability

            roll_input = (ps.ROLL_SETPOINT * ps.MID_INFLUENCE)

            yaw_input = ps.ROLL_SETPOINT

            throttle_input = ps.THROTTLE_SETPOINT
        else:
            self.gate_lost = False
            self.seen_gate_time = time.time()
            variability = abs(mid[0]) + abs(sides_ratio)
            self.last_variability = variability

            roll_input = (- mid[0] * ps.MID_INFLUENCE) - (sides_ratio * ps.SIDES_RATIO_INFLUENCE)

            yaw_input = - mid[0]

            throttle_input = - mid[1]

        if variability < 0.2:                                      # mozna dodac opoznienie np 50 ms
            pitch_input = -0.7
        elif variability < 0.3:
            pitch_input = -0.6
        elif variability < 0.4:
            pitch_input = -0.5
        elif variability < 0.5:
            pitch_input = -0.4
        elif variability < 0.7:
            pitch_input = -0.3
        else:
            pitch_input = -0.2

        self.rollPID.update(roll_input)
        self.yawPID.update(yaw_input)
        self.throttlePID.update(throttle_input)
        self.pitchPID.update(pitch_input)

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
        self.ppm.update_ppm_channels([1500, 1500, 1000, 1500, 1100, 1800, 1000, 1000])
        #if Values.WRITE_TO_FILE:
        #self.file.close()

    def send_ppm(self):
        if self.first_start:
            print("Starting sequence!!")
            self.first_start = False
            self.starting = True
            self.slow_landing = False
            self.seen_gate_time = time.time() + 8
            self.ppm.update_ppm_channels([1500, 1500, 1000, 1500, 1100, 1800, 1000, 1000])
            time.sleep(1)
            self.ppm.update_ppm_channels([1500, 1500, 1000, 1500, 1800, 1800, 1000, 1000])
            time.sleep(1)
            self.ppm.update_ppm_channels([1500, 1500, 1000, 1500, 1800, 1100, 1000, 1000])
            time.sleep(1)
            self.ppm.update_ppm_channels([1500, 1500, 1500, 1500, 1800, 1100, 1000, 1000])
            time.sleep(2)
            self.ppm.update_ppm_channels([1500, 1500, 1500, 1500, 1800, 1100, 1000, 1000])

            self.starting = False
            if Values.WRITE_TO_FILE:
                logging.info("start \n")
            print("Started!!")

        pitch = int(self.pitchPID.output_ppm)
        yaw = int(self.yawPID.output_ppm)
        roll = int(self.rollPID.output_ppm)
        throttle = int(self.throttlePID.output_ppm)

        if not self.hold_possition:
            pitch = 1600

        if self.slow_landing:
            throttle = 1120
            roll = 1500
            pitch = 1500
            yaw = 1500

        if self.gate_lost:
            roll = 1500
            throttle = 1500
            pitch = 1500
            yaw = 1500
            if self.finding_mode == 0:
                yaw = 1600
            elif self.finding_mode == 1:
                yaw = 1400
            elif self.finding_mode == 2:
                yaw = 1400
            elif self.finding_mode == 3:
                yaw = 1600
            elif self.finding_mode == 4:
                pitch = 1600

            if time.time() - self.last_mode_time > 1.8:
                self.last_mode_time = time.time()
                self.finding_mode += 1
                if self.finding_mode > 4:
                    self.finding_mode = 0

        vals = [roll, pitch, throttle, yaw, 1800, 1100, 1000, 1000]
        self.ppm.update_ppm_channels(vals)

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
              str(self.throttlePID.output_ppm)
        logging.info(line)
