
import time
import subprocess
import re

# Start the scheduler
# sched = Scheduler()
# sched.start()

def testSpeed():
    print 'TESTING SPEED'
    p = subprocess.Popen(['speedtest-cli','--simple'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out, err = p.communicate()
    # data = out.split('\n')
    with open("recent_test.txt","w") as fh:
    	fh.write(out)

    


if __name__ == '__main__':
    while True:
        testSpeed()
        time.sleep(30)
