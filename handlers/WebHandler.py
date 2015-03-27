#!/usr/bin/env python
# tuned-resonator
# experiments with google physical-web mdns broadcast

import logging
import datetime
import tornado
import random
from handlers.BaseHandler import BaseHandler
from ResponseObject import ResponseObject
from tornado.template import Template
from tornado.template import Loader

class WebHandler(BaseHandler):
    """HTML display of pingtimes over recent past"""

    def get(self):
        loader = tornado.template.Loader('../speedtest/templates')
        n = self.get_argument('n', 3)
        db = self.settings['db']
        logging.debug('hit the BrowserHandler endpoint with n=', n)
        keywords = []
        found = 0
        keywords = db.lrange('times',0,n)
        print keywords
        self.write(loader.load("speedtest.html").generate(keywords=keywords))
        self.finish()