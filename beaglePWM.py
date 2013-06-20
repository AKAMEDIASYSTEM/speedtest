import BBIO.GPIO as gpio
import BBIO.PWM as pwm

# gonna use P9_14 and P9_16 and P8_13 OR P8_19 for PWM

greenPin = 'P9_14'
bluePin = 'P9_16'
redPin = 'P8_13'

#PWM.start(channel, duty, freq=2000)
pwm.start(greenPin, 50)
pwm.start(bluePin,0)
pwm.start(redPin,0)