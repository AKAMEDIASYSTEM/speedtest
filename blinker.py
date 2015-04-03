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

from blink1 import Blink1
import time
import redis

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
    recent = r_speeds.lrange('times',0,59)
    print recent
    print len(recent)
    pingAv = 0
    ulAv = 0
    dlAv = 0
    for event in recent:
        for entry in event:
            print entry
            if entry=='UL':
                print 'found a UL'
                ulAv+=float(event[entry])
            if entry=='DL':
                dlAv+=float(event[entry])
            if entry=='ping':
                pingAv+=float(event[entry])
        #     print ul
        #     print dl
        #     print ping
    ulAv = ulAv/float(len(recent))
    dlAv = dlAv/float(len(recent))
    pingAv = pingAv/float(len(recent))
    print ulAv, dlAv, pingAv
    b1 = Blink1()
    print 'dlAv is %s' % dlAv
    b1.fade_to_rgb(5000,(255-dlAv),(dlAv), 0)

def mapVals(val, inMin, inMax, outMin, outMax):
    toRet = float(outMin + float(outMax - outMin) * float(float(val - inMin) / float(inMax - inMin)))
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
