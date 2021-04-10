from machine import Pin
from machine import PWM
from machine import ADC
from PID import pid
from pololu import Motor_Driver
from time import sleep

led = Pin(15, Pin.OUT)
button = Pin(14, Pin.IN, Pin.PULL_UP)
pot = ADC(Pin(28))
filter_count = 256

cycle = 0
duty = 65000
freq = 1000
dz_min = -.08
dz_max = .08

motor = Motor_Driver(6,7,8,None,26,27, True)
            #(self, dir_pin, speed_pin, bk_pin, sleep_pin, motor_sense, current_sense, indicator):
motor.speed(freq, duty)
pid = pid()

while True:
    filtered_pot = 0
    for i in range(filter_count):
        filtered_pot += pot.read_u16()
    filtered_pot = filtered_pot / filter_count
    # print(filtered_pot)
    # print(motor.pot_read())
    # print("break")

    print(pot.read_u16())
    print(pid.comp_pid(motor.pot_read(), filtered_pot))
    status = pid.comp_pid(motor.pot_read(), filtered_pot)
    if status < dz_min:
        led.off()
        motor.speed(freq = 1000, duty=65000)
        motor.retract()
    if status > dz_max:
        led.off()
        motor.speed(freq = 1000, duty=65000)
        motor.extend()
    elif status > dz_min and status < dz_max:
        led.on()
        motor.stop()
        print("Stop")
    # sleep(.01)
