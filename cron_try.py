import time
import subprocess
import re

# Start the scheduler
# sched = Scheduler()
# sched.start()
window_size = 29
interval = 30
pingMax = 300 # in ms
dlMax = 20 # in Mb/s
ulMax = 10 # in Mb/s

def testSpeed():
    print 'TESTING SPEED'
    p = subprocess.Popen(['speedtest-cli','--simple'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output, err = p.communicate()
    data = [d for d in output.split('\n') if d.strip()!='']
    # print data
    line = ','.join([
        re.findall(r'[0-9]*\.[0-9]*',entry)[0] 
        for entry in data
    ])
    print line
    out = [line] + [l for l in open("recent_test.txt")][0:window_size]

    open("recent_test.txt","w").write('\n'.join(out))

def mapVals(val, inMin, inMax, outMin, outMax):
	return outMin + (outMax - outMin) * ((val - inMin) / (inMax - inMin))

def updateDevice():
	# make a mapping from most recent speedtest info
	# map dl speed to a red-to-green spectrum
	# map ping time to an angle from 0 to 90 degrees(?)
	# which is 50 steps on a stepper motor...
	# map ul speed to a little pulse
	ping = mapVals(out[0], 0, pingMax, 0, 255)
	dl = mapVals(out[1], 0, dlMax, 0, 255)

if __name__ == '__main__':
    while True:
        testSpeed()
        updateDevice()
        time.sleep(interval)
