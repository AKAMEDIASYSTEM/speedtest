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
interval = 0.01
greenPin = 'P9_14'
bluePin = 'P9_16'
redPin = 'P8_13'

#PWM.start(channel, duty, freq=2000)
# print 'starting pwm channels'
# pwm.start(greenPin, 50.0)
# pwm.start(bluePin, 50.0, 50.0) # 50Hz
# pwm.start(redPin, 0.0)

for j in range(100):
	print j
	print 'starting pwm channels'
	pwm.start(greenPin, 50.0)
	pwm.start(bluePin, 50.0, 50.0) # 50Hz
	pwm.start(redPin, 0.0)
	for i in range(100):
		# print i
		pwm.set_duty_cycle(greenPin, i)
		pwm.start(bluePin, 100-j, 50.0)
		pwm.set_duty_cycle(redPin, 100-i)
		time.sleep(interval)


pwm.cleanup()