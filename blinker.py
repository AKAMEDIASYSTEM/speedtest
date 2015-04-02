#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
import redis
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


EXPIRE_IN = 10800 # this is 3 hours in seconds
window_size = 29 # not using this yet

def do_blink():
    print 'running blinker'
    r_speeds = redis.StrictRedis(host='localhost', port=6379, db=0)
    # get last 60 results (ie LRANGE times 0 59)
    # find max and min
    # scale most recent result to max and min
    # tell blink(1) to be that color

    # pipe = r_speeds.pipeline(transaction=True)
    # redis_response = pipe.incr(url).expire(url, EXPIRE_IN).execute()
    print 'Speedtest beginning:', time.time()
    values = speedtest()
    f = {'ping':"{0:.2f}".format(values[0]), 'DL':"{0:.2f}".format(values[1]), 'UL':"{0:.2f}".format(values[2])}
    # order is pingtime, DL speed, UL speed
    print f
    pipe_speeds = r_speeds.pipeline(transaction=True)
    r_response = pipe_speeds.lpush('times',f).ltrim('times', 0, 179).execute()
    print r_response
    

def mapVals(val, inMin, inMax, outMin, outMax):
    toRet = float(outMin + float(outMax - outMin) * float(float(val - inMin) / float(inMax - inMin)))
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

try:
    do_blink()
except:
    pass
# vim:ts=4:sw=4:expandtab
