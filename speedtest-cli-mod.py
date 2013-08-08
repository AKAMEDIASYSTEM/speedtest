#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2013 Matt Martz
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import urllib2
import math
import time
import os
import sys
import threading
import subprocess
import re
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as pwm
from Queue import Queue
from xml.dom import minidom as DOM
try:
    from urlparse import parse_qs
except ImportError:
    from cgi import parse_qs
try:
    from hashlib import md5
except ImportError:
    from md5 import md5
try:
    from argparse import ArgumentParser as ArgParser
except ImportError:
    from optparse import OptionParser as ArgParser

interval = 60 # in seconds, it turns out!
greenPin = 'P8_13'
bluePin = 'P9_14' # we're not using blue LED, might not even plug it in
redPin = 'P8_19'
servoPin = 'P9_16'

# NOTE, these might be wrong! There's every possiblilty we want
# max=95 and min=90 because the duty cycle is inverted??

servoMax = 10.0
servoMin = 5.0

# from sparkfun small-servo product comments (I think this is my type of servo)
# Here is what I found out with this servo.
# Wiring:
# Red: 5V
# Brown: ground
# Yellow: signal
# Timing: Stable values
# Right at 0.50mS (about 85 degrees)
# Left at 2.0mS (about -85 degrees)
# Center at 1.25ms (about 0 degrees)

window_size = 29 # not using this yet
dlWindow = []
ulWindow = []
pingWindow = []
pingMax = 300 # in ms
dlMax = 20 # in Mb/s, we could divide by 8 to get megabytes/s, which is more common
ulMax = 10 # in Mb/s, we could divide by 8 to get megabytes/s, which is more common
out = []

# Adafruit servo tutorial stuff
duty_min = 3
duty_max = 14.5
duty_span = duty_max - duty_min

# duty = 100 - ((angle_f / 180) * duty_span + duty_min)

def distance(origin, destination):
    """Determine distance between 2 sets of [lat,lon] in km"""

    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371  # km

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1))
         * math.cos(math.radians(lat2)) * math.sin(dlon / 2)
         * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c

    return d


class FileGetter(threading.Thread):
    def __init__(self, url, start):
        self.url = url
        self.result = None
        self.starttime = start
        threading.Thread.__init__(self)

    def get_result(self):
        return self.result

    def run(self):
        try:
            if (time.time() - self.starttime) <= 10:
                f = urllib2.urlopen(self.url)
                self.result = 0
                while 1:
                    contents = f.read(10240)
                    if contents:
                        self.result += len(contents)
                    else:
                        break
                f.close()
            else:
                self.result = 0
        except IOError:
            self.result = 0


def downloadSpeed(files, quiet=False):
    start = time.time()

    def producer(q, files):
        for file in files:
            thread = FileGetter(file, start)
            thread.start()
            q.put(thread, True)
            if not quiet:
                sys.stdout.write('.')
                sys.stdout.flush()

    finished = []

    def consumer(q, total_files):
        while len(finished) < total_files:
            thread = q.get(True)
            thread.join()
            finished.append(thread.result)
            thread.result = 0

    q = Queue(6)
    start = time.time()
    prod_thread = threading.Thread(target=producer, args=(q, files))
    cons_thread = threading.Thread(target=consumer, args=(q, len(files)))
    prod_thread.start()
    cons_thread.start()
    prod_thread.join()
    cons_thread.join()
    return (sum(finished)/(time.time()-start))


class FilePutter(threading.Thread):
    def __init__(self, url, start, size):
        self.url = url
        data = os.urandom(int(size)).encode('hex')
        self.data = 'content1=%s' % data[0:int(size)-9]
        del data
        self.result = None
        self.starttime = start
        threading.Thread.__init__(self)

    def get_result(self):
        return self.result

    def run(self):
        try:
            if (time.time() - self.starttime) <= 10:
                f = urllib2.urlopen(self.url, self.data)
                contents = f.read()
                f.close()
                self.result = len(self.data)
            else:
                self.result = 0
        except IOError:
            self.result = 0


def uploadSpeed(url, sizes, quiet=False):
    start = time.time()

    def producer(q, sizes):
        for size in sizes:
            thread = FilePutter(url, start, size)
            thread.start()
            q.put(thread, True)
            if not quiet:
                sys.stdout.write('.')
                sys.stdout.flush()

    finished = []

    def consumer(q, total_sizes):
        while len(finished) < total_sizes:
            thread = q.get(True)
            thread.join()
            finished.append(thread.result)
            thread.result = 0

    q = Queue(6)
    start = time.time()
    prod_thread = threading.Thread(target=producer, args=(q, sizes))
    cons_thread = threading.Thread(target=consumer, args=(q, len(sizes)))
    prod_thread.start()
    cons_thread.start()
    prod_thread.join()
    cons_thread.join()
    return (sum(finished)/(time.time()-start))


def getAttributesByTagName(dom, tagName):
    elem = dom.getElementsByTagName(tagName)[0]
    return dict(elem.attributes.items())


def getConfig():
    """Download the speedtest.net configuration and return only the data
    we are interested in
    """

    uh = urllib2.urlopen('http://www.speedtest.net/speedtest-config.php')
    configxml = uh.read()
    if int(uh.code) != 200:
        return None
    uh.close()
    root = DOM.parseString(configxml)
    config = {
        'client': getAttributesByTagName(root, 'client'),
        'times': getAttributesByTagName(root, 'times'),
        'download': getAttributesByTagName(root, 'download'),
        'upload': getAttributesByTagName(root, 'upload')}

    del root
    return config


def closestServers(client, all=False):
    """Determine the 5 closest speedtest.net servers based on geographic
    distance
    """

    uh = urllib2.urlopen('http://www.speedtest.net/speedtest-servers.php')
    serversxml = uh.read()
    if int(uh.code) != 200:
        return None
    uh.close()
    root = DOM.parseString(serversxml)
    servers = {}
    for server in root.getElementsByTagName('server'):
        attrib = dict(server.attributes.items())
        d = distance([float(client['lat']), float(client['lon'])],
                     [float(attrib.get('lat')), float(attrib.get('lon'))])
        attrib['d'] = d
        if d not in servers:
            servers[d] = [attrib]
        else:
            servers[d].append(attrib)
    del root

    closest = []
    for d in sorted(servers.keys()):
        for s in servers[d]:
            closest.append(s)
            if len(closest) == 5 and not all:
                break
        else:
            continue
        break

    del servers
    return closest


def getBestServer(servers):
    """Perform a speedtest.net "ping" to determine which speedtest.net
    server has the lowest latency
    """

    results = {}
    for server in servers:
        cum = 0
        url = os.path.dirname(server['url'])
        for i in xrange(0, 3):
            uh = urllib2.urlopen('%s/latency.txt' % url)
            start = time.time()
            text = uh.read().strip()
            total = time.time() - start
            if int(uh.code) == 200 and text == 'test=test':
                cum += total
            else:
                cum += 3600
            uh.close()
        avg = round((cum / 3) * 1000000, 3)
        results[avg] = server

    fastest = sorted(results.keys())[0]
    best = results[fastest]
    best['latency'] = fastest

    return best


def speedtest():
    """Run the full speedtest.net test"""

    description = (
        'Command line interface for testing internet bandwidth using '
        'speedtest.net.\n'
        '------------------------------------------------------------'
        '--------------\n'
        'https://github.com/sivel/speedtest-cli')

    parser = ArgParser(description=description)
    try:
        parser.add_argument = parser.add_option
    except AttributeError:
        pass
    parser.add_argument('--share', action='store_true',
                        help='Generate and provide a URL to the speedtest.net '
                             'share results image')
    parser.add_argument('--simple', action='store_true',
                        help='Suppress verbose output, only show basic '
                             'information')
    parser.add_argument('--list', action='store_true',
                        help='Display a list of speedtest.net servers '
                             'sorted by distance')
    parser.add_argument('--server', help='Specify a server ID to test against')
    parser.set_defaults(simple=True) # added this to simplify importing this script
    options = parser.parse_args()
    if isinstance(options, tuple):
        args = options[0]
    else:
        args = options
    del options
    output = []
    if not args.simple:
        print 'Retrieving speedtest.net configuration...'
    config = getConfig()

    if not args.simple:
        print 'Retrieving speedtest.net server list...'
    if args.list or args.server:
        servers = closestServers(config['client'], True)
        if args.list:
            serverList = []
            for server in servers:
                line = ('%(id)4s) %(sponsor)s (%(name)s, %(country)s) '
                        '[%(d)0.2f km]' % server)
                serverList.append(line)
            try:
                print '\n'.join(serverList).encode('utf-8', 'ignore')
            except IOError:
                pass
            sys.exit(0)
    else:
        servers = closestServers(config['client'])

    if not args.simple:
        print 'Testing from %(isp)s (%(ip)s)...' % config['client']

    if args.server:
        try:
            best = getBestServer(filter(lambda x: x['id'] == args.server,
                                        servers))
        except IndexError:
            print 'Invalid server ID'
            sys.exit(1)
    else:
        if not args.simple:
            print 'Selecting best server based on ping...'
        best = getBestServer(servers)

    if not args.simple:
        print ('Hosted by %(sponsor)s (%(name)s) [%(d)0.2f km]: '
               '%(latency)s ms' % best)
    else:
        print 'Ping: %(latency)s ms' % best
        output.append(best['latency'])
        print 'best is ', best

    sizes = [350, 500, 750, 1000, 1500, 2000, 2500, 3000, 3500, 4000]
    urls = []
    for size in sizes:
        for i in xrange(0, 4):
            urls.append('%s/random%sx%s.jpg' %
                        (os.path.dirname(best['url']), size, size))
    if not args.simple:
        print 'Testing download speed',
    dlspeed = downloadSpeed(urls, args.simple)
    if not args.simple:
        print
    print 'Download: %0.2f Mbit/s' % ((dlspeed / 1000 / 1000) * 8)
    output.append(((dlspeed / 1000 / 1000) * 8))

    sizesizes = [int(.25 * 1000 * 1000), int(.5 * 1000 * 1000)]
    sizes = []
    for size in sizesizes:
        for i in xrange(0, 25):
            sizes.append(size)
    if not args.simple:
        print 'Testing upload speed',
    ulspeed = uploadSpeed(best['url'], sizes, args.simple)
    if not args.simple:
        print
    print 'Upload: %0.2f Mbit/s' % ((ulspeed / 1000 / 1000) * 8)
    output.append(((ulspeed / 1000 / 1000) * 8))

    if args.share:
        dlspeedk = int(round((dlspeed / 1000) * 8, 0))
        ping = int(round(best['latency'], 0))
        ulspeedk = int(round((ulspeed / 1000) * 8, 0))

        apiData = [
            'download=%s' % dlspeedk,
            'ping=%s' % ping,
            'upload=%s' % ulspeedk,
            'promo=',
            'startmode=%s' % 'pingselect',
            'recommendedserverid=%s' % best['id'],
            'accuracy=%s' % 1,
            'serverid=%s' % best['id'],
            'hash=%s' % md5('%s-%s-%s-%s' %
                            (ping, ulspeedk, dlspeedk, '297aae72')
                            ).hexdigest()]

        req = urllib2.Request('http://www.speedtest.net/api/api.php',
                              data='&'.join(apiData))
        req.add_header('Referer', 'http://c.speedtest.net/flash/speedtest.swf')
        f = urllib2.urlopen(req)
        response = f.read()
        code = f.code
        f.close()

        if int(code) != 200:
            print 'Could not submit results to speedtest.net'
            sys.exit(1)

        qsargs = parse_qs(response)
        resultid = qsargs.get('resultid')
        if not resultid or len(resultid) != 1:
            print 'Could not submit results to speedtest.net'
            sys.exit(1)

        print ('Share results: http://www.speedtest.net/result/%s.png' %
               resultid[0])
    return output

def testSpeed():
    pwm.start(bluePin,50,60.0)
    print 'TESTING SPEED'
    values = speedtest()
    pingtime = mapVals(float(values[0]),0,1000,10,170) #changed to 160 deg total rot to be safe
    dl = mapVals(float(values[1]),0, dlMax, 0, 100)
    ul = mapVals(float(values[2]),0, ulMax, 0, 100)
    pwm.set_duty_cycle(greenPin,100.0-dl)
    pwm.set_duty_cycle(redPin,dl)
    # pwm.start(servoPin, 60.0)
    # servo(servoPin, pingtime)
    print 'pingtime in servo degrees is', pingtime
    print 'dl is %s percent red', dl
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
    # min -90deg, we are guessing this is a 1ms pulse
    # 1ms pulse is 5% duty cycle
    # max 90deg, we are guessing this is a 2ms pulse
    # 2ms pulse is 10% duty cycle
    # we are guessing it's a 50Hz (20ms) base freq
    duty = 100 - ((position / 180) * duty_span + duty_min)
    # rot = mapVals(position,0,180,servoMin, servoMax)
    print 'duty should be', duty
    pwm.set_duty_cycle(pinName, (100-duty_min))

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
    # print os.system('whoami')
    # print 'starting pwm channels'
    pwm.start(greenPin, 10, 2000.0)
    # pwm.start(bluePin,0, 60.0)
    pwm.start(redPin,10, 2000.0)
    # time.sleep(15)
    # print 'done starting pwm channels'
    while True:
        try:
            testSpeed()
        except:
            pass
        time.sleep(interval)

# vim:ts=4:sw=4:expandtab
