import tornado.ioloop
import tornado.web
import tornado.options
import re
import subprocess
import json
import logging

settings = {'debug':True}
db = redis.StrictRedis(host='localhost', port=6379, db=0)

class MainHandler(tornado.web.RequestHandler):
    # data = []
    # p = subprocess.Popen(['speedtest-cli','--simple'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    # out, err = p.communicate()
    # data = re.split(r'\n',out)

    def get(self):
        # self.write("Hello, buddy")
        with open("recent_test.txt") as fh:
            stats = [line.strip() for line in fh]
            logging.info(stats)
            # self.write('<br/>'.join(stats))
            self.write('+')
            for entry in stats:
                nums = re.findall(r'[0-9]*\.[0-9]*',entry)
                self.write(''.join(nums))
                self.write('|')
                logging.info(str(nums))
            self.write('?')

application = tornado.web.Application([
    (r"/", MainHandler),
], db=db, **settings)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()




#rough speedtest-to-server idea



# p = subprocess.Popen(['speedtest-cli','--simple'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
# out, err = p.communicate()
# print out

# data = re.split(r'\n',out)
# for entry in data:
# 	# strip everything that isn't a number
# 	# order is ping, download, upload
# 	print re.findall(r'[0-9]*\.[0-9]*',entry)

# ok, now do this every 5 minutes and serve out the result via tornado