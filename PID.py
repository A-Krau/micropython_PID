from time import sleep
import time

"""Code rewritten in python from...
https://www.teachmemicro.com/arduino-pid-control-tutorial/
"""

class pid():
    """My attempt at writing a PID class"""
    def __init__(self):

        self.previous_time = 0
        self.set_point = 0
        self.cumu_error = 0
        self.last_error = 0

        self.kp = 0.0003
        self.ki = 0
        self.kd = 0.005
        
        #print in the terminal to make sure my upload actually took and the values were updated.
        print(self.kp, self.ki, self.kd)

    """To tune a PID use the following steps:
    1.Set all gains to zero.
    2. Increase the P gain until the response to a disturbance is steady oscillation.
    3. Increase the D gain until the the oscillations go away (i.e. it's critically damped).
    4. Repeat steps 2 and 3 until increasing the D gain does not stop the oscillations.
    5. Set P and D to the last stable values.
    6. Increase the I gain until it brings you to the setpoint with the number of oscillations 
        desired (normally zero but a quicker response can be had if you don't mind a couple 
        oscillations of overshoot)

    This worked best for me and was found here...
    https://robotics.stackexchange.com/questions/167/what-are-good-strategies-for-tuning-pid-loops
    """        


    def comp_pid(self, sensor_pos, set_point):
        """Compute PID value based on a sensors postion and a given set point.  
        sensor_pos and set_point must be on the same scale.
        """

        self.cur_time = time.ticks_ms()
        self.elapsed_time = (self.cur_time - self.previous_time)

        self.error = set_point - sensor_pos
        self.cumu_error += self.error * self.elapsed_time
        try:
            self.rate_error = (self.error - self.last_error)/self.elapsed_time
        #except the zero error I was getting at times
        except:
            pass
            
        self.out = self.kp*self.error + self.ki*self.cumu_error + self.kd*self.rate_error

        self.last_error = self.error
        self.previous_time = self.cur_time

        return float(self.out)

