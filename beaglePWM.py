import BBIO.GPIO as gpio
import BBIO.PWM as pwm
import time

# gonna use P9_14 and P9_16 and P8_13 OR P8_19 for PWM
interval = 0.3
greenPin = 'P9_14'
bluePin = 'P9_16'
redPin = 'P8_13'

#PWM.start(channel, duty, freq=2000)
print 'starting pwm channels'
pwm.start(greenPin, 50)
pwm.start(bluePin,0)
pwm.start(redPin,0)

for i in range(100):
	print i
	pwm.set_duty_cycle(greenPin, i)
	pwm.set_duty_cycle(bluePin, 100-i)
	pwm.set_duty_cycle(redPin, i)
	time.sleep(interval)

pwm.cleanup()