import tornado.ioloop
import tornado.web
import tornado.options
import re
import subprocess
import json
import logging
from handlers.BrowserHandler import BrowserHandler
from handlers.ApiHandler import ApiHandler

settings = {'debug':True}
db = redis.StrictRedis(host='localhost', port=6379, db=0)

application = tornado.web.Application([
    (r"/", WebHandler),
    (r"/api",ApiHandler),
], db=db, **settings)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()