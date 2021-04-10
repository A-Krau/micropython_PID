from time import sleep
import time

class pid():
    """My attempt at writing a PID program"""
    def __init__(self):
        self.cur_time = 0
        self.elapsed_time = 0
        self.previous_time = 0
        self.set_point = 0
        self.error = 0
        self.cumu_error = 0
        self.rate_error = 0
        self.last_error = 0
        self.out = 0

        self.kp = 1
        self.ki = 0
        self.kd = .1
        
        print(self.kp, self.ki, self.kd)
        time.sleep(1)

    def comp_pid(self, sensor_pos, set_point):
        self.cur_time = time.ticks_ms()
        self.elapsed_time = (self.cur_time - self.previous_time)

        self.error = set_point - sensor_pos
        self.cumu_error += self.error * self.elapsed_time
        try:
            self.rate_error = (self.error - self.last_error)/self.elapsed_time
        except:
            pass
            
        self.out = self.kp*self.error + self.ki*self.cumu_error + self.kd*self.rate_error

        self.last_error = self.error
        self.previous_time = self.cur_time

        return int(self.out)

