#!/usr/bin/env python
#
# -*- coding: utf-8 -*-
#from string import Template
#
import temstand
#
import redis

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8000,help="nothing",type=int)

class ApiHandler(tornado.web.RequestHandler):
    def post  


if __name__ == '__main__':

    r = redis.StrictRedis()
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/",IndexHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


