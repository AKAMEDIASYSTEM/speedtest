#!/usr/bin/env python
# speedtest - tuned-resonator barnacle
# (c)nytlabs 2015

import tornado
import tornado.ioloop
import tornado.web
import tornado.options
import tornado.template
import ResponseObject
import traceback


class BaseHandler(tornado.web.RequestHandler):

    def __init__(self, *args, **kwargs):
        # logging.debug('entering init funciton of BaseHandler')
        try:
            tornado.web.RequestHandler.__init__(self,  *args, **kwargs)
            self.set_header("Access-Control-Allow-Origin", "*")
            self.response = ResponseObject.ResponseObject()
        except Exception as reason:
            print reason, traceback.format_exc()

    def write_response(self):
        try:
            self.write(self.response.response)
        except Exception as reason:
            print reason, traceback.format_exc()
            print self.response.response
