#!/usr/bin/env python
# tuned-resonator
# experiments with google physical-web mdns broadcast

import logging
import tornado
from handlers.BaseHandler import BaseHandler
import ast


class WebHandler(BaseHandler):
    """HTML display of pingtimes over recent past"""

    def mapVals(self, val, inMin, inMax, outMin, outMax):
        toRet = outMin + (outMax-outMin)*((val-inMin)/float(inMax-inMin))
        return toRet

    def clamp(self, val, minv, maxv):
        if (val < minv):
            val = minv
        if (val > maxv):
            val = maxv
        return val

    def mean(self, inp):
        summ = 0
        for i in inp:
            summ += float(i)
        summ = summ/float(len(inp))
        return summ

    def get(self):
        loader = tornado.template.Loader('../speedtest/templates')
        db = self.settings['db']
        logging.debug('hit the BrowserHandler endpoint')
        recent = db.lrange('times', 0, 59)
        pingAv = []
        ulAv = []
        dlAv = []
        for event in recent:
            # redis stores dict as a string, this is working ok to re-dict
            event = ast.literal_eval(event)
            for entry in event:
                if entry == 'UL':
                    ulAv.append(float(event[entry]))
                if entry == 'DL':
                    dlAv.append(float(event[entry]))
                if entry == 'ping':
                    pingAv.append(float(event[entry]))
        current = ast.literal_eval(recent[0])
        print current
        ulOutput = self.mapVals(float(current['UL']), min(ulAv), max(ulAv), 0.0, 255.0)
        dlOutput = self.mapVals(float(current['DL']), min(dlAv), max(dlAv), 0, 255)
        pingOutput = 10.0*self.mapVals(float(current['ping']), min(pingAv), max(pingAv), 0, 255)  # times 10 just for pingtime to be noticeable
        print ulOutput, dlOutput, pingOutput
        tcolor = [ulOutput,dlOutput]
        keywords = [current]
        print 'keywords is ', keywords
        self.write(loader.load("speedtest.html").generate(keywords=keywords, color=tcolor))
        self.finish()
