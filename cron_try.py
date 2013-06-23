import time
import subprocess
import re
import BBIO.GPIO as GPIO
import BBIO.PWM as pwm

# from source on github:
# PWM_PINS = {
#     "PWM1A" : {"key":"P9_14"},
#     "PWM1B" : {"key":"P9_16"},
#     "PWM2A" : {"key":"P8_45"},
#     "PWM2B" : {"key":"P8_13"}
#   }
# but for some reason they don't work. Mismatch between adafruit lib and branch it forked from?

interval = 60 # in seconds, it turns out!
greenPin = 'P9_14'
bluePin = 'P9_16' # we're not using blue LED, might not even plug it in - in that case use this for servo
redPin = 'P8_13'
servoPin = 'P8_45'

window_size = 29
pingMax = 300 # in ms
dlMax = 20 # in Mb/s, we could divide by 8 to get megabytes/s, which is more common
ulMax = 10 # in Mb/s, we could divide by 8 to get megabytes/s, which is more common
out = []

def testSpeed():
    pwm.start(bluePin,50)
    print 'TESTING SPEED'
    p = subprocess.Popen(['speedtest-cli','--simple'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output, err = p.communicate()
    data = [d for d in output.split('\n') if d.strip()!='']
    print 'data is ', data
    line = ','.join([
        re.findall(r'[0-9]*\.[0-9]*',entry)[0] 
        for entry in data
    ])
    # print line
    values = line.split(',')
    print 'values is ', values
    pingtime = mapVals(float(values[0]),0,1000,0,180)
    dl = mapVals(float(values[1]),0, dlMax, 0, 100)
    ul = mapVals(float(values[2]),0, ulMax, 0, 100)
    pwm.start(greenPin,100-dl)
    pwm.start(redPin,dl)
    # pwm.start(bluePin, pingtime)
    servo(bluePin, pingtime)
    print 'pingtime is', pingtime
    print 'dl is', dl
    # updateDevice(pingtime, dl, ul)
    # out = [line] + [l for l in open("recent_test.txt")][0:window_size]
    # open("recent_test.txt","w").write('\n'.join(out))

def mapVals(val, inMin, inMax, outMin, outMax):
    toRet = outMin + (outMax - outMin) * ((val - inMin) / (inMax - inMin))
    # if (toRet > outMax):
    #     toRet = outMax
    # if (toRet < outMin):
    #     toRet = outMin
    return clamp(toRet, outMin, outMax)

def clamp(val, min, max):
    if (val < min):
        val = min
    if (val > max):
        val = max
    return val

def servo(pinName,position):
    # position should be 0-180, with 90 and center
    # min -90, we are guessing this is a 1ms pulse
    # 1ms pulse is 5% duty cycle
    # max 90, we are guessing this is a 2ms pulse
    # 2ms pulse is 10% duty cycle
    # we are guessing it's a 50Hz (20ms) base freq
    rot = mapVals(position,0,180,5, 10)
    if (rot < 0): rot = 0
    if (rot > 180): rot = 180
    pwm.start(pinName, rot)

def updateDevice(pingtime, dls, uls):
    ping = mapVals(pingtime, 0, pingMax, 0, 255)
    dl = mapVals(out, 0, dlMax, 0, 255)
    # we don't do anything with ul yet
    pwm.start(redPin, 100-dl)
    pwm.start(greenPin, dl)
    # make a mapping from most recent speedtest info
	# map dl speed to a red-to-green spectrum
	# map ping time to an angle from 0 to 90 degrees(?)
	# which is 50 steps on a stepper motor...
	# map ul speed to a little pulse


if __name__ == '__main__':
    #PWM.start(channel, duty, freq=2000)
    print 'starting pwm channels'
    pwm.start(greenPin, 0)
    pwm.start(bluePin,0)
    pwm.start(redPin,0)
    print 'done starting pwm channels'
    while True:
        testSpeed()
        time.sleep(interval)
