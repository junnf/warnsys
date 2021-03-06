#!/usr/bin/env python
#
# -*- coding: utf-8 -*-
#from string import Template
#
import temstand
import json
#
import pymongo

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8000,help="nothing",type=int)

class Application(tornado.web.Application):
    def __init__(self):
      
        handlers = [
      (r"/api", ApiHandler),
      (r"/api/condition", ConditionHandler),
      (r"/api/conditionpeople/source", ConditionPeopleHandler),
      (r"/test",TestHandler)
      ]
        conn = pymongo.Connection("localhost", 27017)
        self.db = conn["warn_set"]
        tornado.web.Application.__init__(self, handlers, debug=True)

class TestHandler(tornado.web.RequestHandler):
    def get(self):
      #a = self.get_argument('xxx')  
        self.write(self.request.body)

class ApiHandler(tornado.web.RequestHandler):
  #def post(): 
   #     pass   
    def get(self):
      #self.write("aa")
        _api_list = {'api_num': 7,
            'api_list': ({
                  'notify':'url',
                  #post message (email,mobi)
                  'notify_condition':'url',
                  'add_condition':'url',
                  'add_condition_people':'url',
                  'del_condition':'url',
                  'del_condition_people':'url',
                  #fin get warning condition
                  'condition':'url api/condition'
              })
            }
        #separators=(',', ': '),
        api_list = json.dumps(_api_list,indent=4)
        #print api_list
        self.write(api_list)
       
class NotifyHandler(tornado.web.RequestHandler):
    def post(self):
        _condition = self.get_argument('condition')
        #(email,mobi) from mongodb get
        pass
        #test api

class ConditionHandler(tornado.web.RequestHandler):
  
    #(r"/api/condition", ConditionHandler),
    def get(self):
        #get data 
        #warn_set
        coll = self.application.db.warn_set
        #elems_coll = coll.find({},{"condition_name" : 1,"_id" : 0})
        condition_list = coll.distinct('condition_name') 
        self.write(json.dumps(condition_list))
   
    def post(self):
        _condition_name = self.get_argument('condition_name')
        #test
        #print (_condition_name == u"")
        #print _condition_name
         #self.get_argument()
        _tem_dict = {}
        if _condition_name != u'':
            coll = self.application.db.warn_set    
            if coll.find({ 'condition_name' : _condition_name }) == None:
                _tem_dict['condition_name'] = _condition_name
                coll.insert(_tem_dict)
       

class ConditionPeopleHandler(tornado.web.RequestHandler):
    
    '''(r"/api/conditionpeople/source", ConditionPeopleHandler)'''
    
    def get(self):
        
        _cond_name = self.get_argument('cond_name')
        _tem_people_dict = {}
        if _cond_name != u'':
            coll = self.application.db[_cond_name]
            for x in coll.find():
                _tem_people_dict[x[u'name']] = {
                    'name':x['name'],
                    'email':x['email'],
                    'mobi':x['mobi']
                    }
                self.write(json.dumps(_tem_people_dict))

        #get condition people
        #pass   

    def post(self):
        
        #url
        _cond_name_set = self.get_argument('condition')
        _person = self.get_argument('person')
        _email = self.get_argument('email')
        _mobi = self.get_argument('mobi')
        _tem_people_dict = {}
        #if _person != u'' and ( _email != u'' or _mobi != u''):
        coll = self.application.db[_cond_name_set]
            #for _record in coll.find({'name':_person}):
        if coll.find({'name' : _person}) == None:
            coll.insert({'name':_person, 'email':_email, 'mobi':_mobi})
        self.write(json.dumps({'person':_person,'email':_email,'mobi':_mobi}))

if __name__ == '__main__':

    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


