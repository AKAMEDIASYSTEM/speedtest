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
import redis
import ast

def do_blink():
    print 'running blinker'
    r_speeds = redis.StrictRedis(host='localhost', port=6379, db=0)
    # get last 60 results (ie LRANGE times 0 59)
    # find max and min
    # scale most recent result to max and min
    # tell blink(1) to be that color
    recent = r_speeds.lrange('times',0,59)
    pingAv = []
    ulAv = []
    dlAv = []
    for event in recent:
        # redis stores dict as a string, this is working ok to re-dict
        event = ast.literal_eval(event)
        for entry in event:
            if entry=='UL':
                ulAv.append(float(event[entry]))
            if entry=='DL':
                dlAv.append(float(event[entry]))
            if entry=='ping':
                pingAv.append(float(event[entry]))
    current = ast.literal_eval(recent[0])
    print current
    ulOutput = mapVals(float(current['UL']), min(ulAv), max(ulAv),0.0,255.0)
    dlOutput = mapVals(float(current['DL']), min(dlAv),max(dlAv),0,255)
    pingOutput = 10.0*mapVals(float(current['ping']), min(pingAv),max(pingAv),0,255) # times 10 just for pingtime to be noticeable
    print ulOutput, dlOutput, pingOutput
    b1 = Blink1()
    b1.fade_to_rgb(int(pingOutput),int(255-dlOutput),int(dlOutput), 0)

def mapVals(val, inMin, inMax, outMin, outMax):
    toRet = outMin+ (outMax-outMin)*((val-inMin)/float(inMax-inMin))
    return toRet

def clamp(val, minv, maxv):
    if (val < minv):
        val = minv
    if (val > maxv):
        val = maxv
    return val

def mean(inp):
    summ = 0;
    for i in inp:
        summ+=float(i)
    summ = summ/float(len(inp))
    return summ
try:
    do_blink()
except:
    pass
# vim:ts=4:sw=4:expandtab
