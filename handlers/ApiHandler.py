#!/usr/bin/env python
# tuned-resonator
# experiments with google physical-web mdns broadcast

import logging
import tornado
from handlers.BaseHandler import BaseHandler
from ResponseObject import ResponseObject

class ApiHandler(BaseHandler):
    """json access to local speedtest store"""

    def get(self):
        try:
            n = self.get_argument('n',10) # return 10 if n is None
            n = int(n)
            if n < 1:
                n = 1
        except:
            n = 10 # deliver the last ten results by default
        db = self.settings['db']
        print 'hit the ApiHandler endpoint with n=', n
        k = db.lrange('times',0,n-1)
        if k is not None:
            print k
        else:
            pass
        d = {'title':'tuned-resonator speedtest-barnacle test',
        'results':k}
        self.response = ResponseObject('200','Success', d)
        self.write_response()
        self.finish()