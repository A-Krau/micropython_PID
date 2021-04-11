from machine import Pin
from machine import PWM
from machine import ADC
from PID import pid
from pololu import Motor_Driver
from time import sleep

led = Pin(15, Pin.OUT)
button = Pin(14, Pin.IN, Pin.PULL_UP)
pot = ADC(Pin(28))
pot_filter_count = 256
filter_count = 1

cycle = 0
duty = 65000
freq = 1000
dz_min = -.08
dz_max = .08

motor = Motor_Driver(6,7,8,None,26,None, True)
            #(self, dir_pin, speed_pin, bk_pin, sleep_pin, motor_sense, current_sense, indicator):
motor2 = Motor_Driver(16, 17, None, None, 27, None, None)
motor.speed(freq, duty)
motor2.speed(freq, duty)
pid_1 = pid()
pid_2 = pid()

while True:
    filtered_pot = 0
    for i in range(pot_filter_count):
        filtered_pot += pot.read_u16()
    filtered_pot = filtered_pot / pot_filter_count
    filtered_motor = 0
    for i in range(filter_count):
        filtered_motor += motor.pot_read()
    filtered_motor = filtered_motor/filter_count
    # print(filtered_pot)
    # print(motor.pot_read())
    # print("break")

    print(pot.read_u16())
    print(pid_1.comp_pid(motor.pot_read(), filtered_pot))
    status = pid_1.comp_pid(motor.pot_read(), filtered_pot)
    status2 = pid_2.comp_pid(motor2.pot_read(), filtered_motor)

    if status < dz_min:
        led.off()
        motor.speed(freq = 1000, duty=65000)
        motor.retract()
    if status > dz_max:
        led.off()
        motor.speed(freq = 1000, duty=65000)
        motor.extend()
    if status > dz_min and status < dz_max:
        led.on()
        motor.stop()
        print("Stop")

    #motor 2 stuff.
    if status2 < dz_min:
        #led.off()
        motor2.speed(freq = 1000, duty=65000)
        motor2.retract()
    if status2 > dz_max:
        #led.off()
        motor2.speed(freq = 1000, duty=65000)
        motor2.extend()
    if status2 > dz_min and status2 < dz_max:
        #led.on()
        motor2.stop()
        print("Stop")
    
    
    #sleep(.01)