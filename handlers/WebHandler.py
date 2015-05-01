#!/usr/bin/env python
# tuned-resonator
# experiments with google physical-web mdns broadcast

import logging
import tornado
from handlers.BaseHandler import BaseHandler
import ast


class WebHandler(BaseHandler):
    """HTML display of pingtimes over recent past"""

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
        keywords = []
        print keywords
        self.write(loader.load("speedtest.html").generate(keywords=keywords))
        self.finish()
