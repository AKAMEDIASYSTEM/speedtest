import BBIO.GPIO as gpio
import BBIO.PWM as pwm
import time

# gonna use P9_14 and P9_16 and P8_13 OR P8_19 for PWM
interval = 500
greenPin = 'P9_14'
bluePin = 'P9_16'
redPin = 'P8_13'

#PWM.start(channel, duty, freq=2000)
pwm.start(greenPin, 50)
pwm.start(bluePin,0)
pwm.start(redPin,0)

for i in range(100):
	print i
	pwm.start(greenPin, i)
	pwm.start(bluePin, 100-i)
	pwm.start(redPin, 0)
	time.sleep(interval)

