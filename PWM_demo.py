import time
import Adafruit_BBIO.PWM as pwm
import atexit

redPin = 'P8_19'
greenPin = 'P8_13'
interval = 0.25
pwm.start(redPin,50,2000)
pwm.start(greenPin,50,2000)

def exit_handler():
    print 'exiting'
    pwm.stop(greenPin)
    pwm.stop(redPin)
    pwm.cleanup()

atexit.register(exit_handler)

while True:
	for i in range(0,100):
		pwm.set_duty_cycle(redPin,float(i))
		pwm.set_duty_cycle(greenPin,100.0-i)
		time.sleep(interval)
	for i in range(0,100):
		pwm.set_duty_cycle(redPin,100.0-i)
		pwm.set_duty_cycle(greenPin,float(i))
		time.sleep(interval)