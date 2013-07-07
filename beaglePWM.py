import Adafruit_BBIO.GPIO as gpio
import Adafruit_BBIO.PWM as pwm
import time

# from source on github:
# PWM_PINS = {
#     "PWM1A" : {"key":"P9_14"},
#     "PWM1B" : {"key":"P9_16"},
#     "PWM2A" : {"key":"P8_45"},
#     "PWM2B" : {"key":"P8_13"}
#   }
interval = .1
greenPin = 'P9_14'
bluePin = 'P9_16'
redPin = 'P8_13'

def mapVals(val, inMin, inMax, outMin, outMax):
    toRet = outMin + ((outMax - outMin) * ((val - inMin) / (inMax - inMin)))
    if (toRet > outMax):
        toRet = outMax
    if (toRet < outMin):
        toRet = outMin
    # print 'toRet is ',toRet
    return toRet

#PWM.start(channel, duty, freq=2000)

while True:
	print 'starting pwm channels'
	pwm.start(greenPin, 99.0, 50)
	pwm.start(bluePin, 99.0, 50) # 50Hz
	pwm.start(redPin, 99.0, 50)
	for j in range(100):
		print j
		rot = mapVals(j,0.0,100.0,90.0,95.0)
		# rot = mapVals(j,0.0,100.0,5.0,10.0)
		print rot
		pwm.set_duty_cycle(greenPin, 100-j)
		pwm.set_duty_cycle(bluePin, rot) # 50Hz
		# pwm.set_frequency(bluePin, 50.0)
		# pwm.set_duty_cycle(bluePin, rot)
		pwm.set_duty_cycle(redPin, j)

		# rot = mapVals(j,0.0,100.0,5.0,20.0)
		# print 'rot is',rot
		# pwm.set_duty_cycle(bluePin, rot) # servo ms timing experiment
		time.sleep(interval)
		# for i in range(100):
		# 	# print i
			
		# 	pwm.set_duty_cycle(greenPin, i)
			
		# 	pwm.set_duty_cycle(redPin, 100-i)
		# 	time.sleep(interval)


	pwm.cleanup()

