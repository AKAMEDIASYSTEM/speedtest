import BBIO.GPIO as gpio
import BBIO.PWM as pwm
import time

# from source on github:
# PWM_PINS = {
#     "PWM1A" : {"key":"P9_14"},
#     "PWM1B" : {"key":"P9_16"},
#     "PWM2A" : {"key":"P8_45"},
#     "PWM2B" : {"key":"P8_13"}
#   }
# gonna use P9_14 and P9_16 and P8_13 OR P8_19 for PWM
interval = 0.01
greenPin = 'PWM1A'
bluePin = 'PWM1B'
redPin = 'PWM2B'

#PWM.start(channel, duty, freq=2000)
print 'starting pwm channels'
pwm.start(greenPin, 50)
pwm.start(bluePin,0)
pwm.start(redPin,0)

for j in range(100):
	print j
	for i in range(100):
		# print i
		pwm.start(greenPin, i)
		# pwm.start(bluePin, 100-i)
		pwm.start(redPin, 100-i)
		time.sleep(interval)
pwm.cleanup()