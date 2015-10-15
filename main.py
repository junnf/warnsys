#!/usr/bin/env python
#

# -*- coding: utf-8 -*-

#from string import Template
#
import json
#
import pymongo

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

import sendcloud.sendemail, sendcloud.sendemail

from tornado.options import define, options

#import sendcloud.sendemail
from sendcloud import sendemail
import sendcloud.sendmessage


define("port", default=8000,help="nothing",type=int)

class Application(tornado.web.Application):
    def __init__(self):
      
        handlers = [
            #      (r"/api", ApiHandler),
            #      (r"/api/condition", ConditionHandler),
            #      (r"/api/conditionpeople/source", ConditionPeopleHandler),
            #      (r"/test",TestHandler)
            (r"/api/post",  TongzhiHandler),
      ]
        conn = pymongo.Connection("localhost", 27017)
        self.db = conn["member"]
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
        '''_condition = self.get_argument('cond')
        coll = self.application.db.warn_set
        _notify = coll.find_one({'con_nam':_condition})
        coll1 = self.application.db[_notify]
        #pass message
        _content = _notify['con_des']
        for _item in coll1.find():
        #(email,mobi) from mongodb get
        pass
        #test api
        '''


class TongzhiHandler(tornado.web.RequestHandler):
    def post(self):
        '''
        {
          name:
          email:
          mobi:
          }

        '''
        _cond = self.get_argument('cond')
        _cond_des = self.get_argument('cond_des')
        coll = self.application.db['member']
        for _tem_meb in coll.find():
          #notify
            _pos_par = sendemail.get_params(emailto = str(_tem_meb['email']),
                emailfrom = 'error_alert@sendcloud.org',
                fromname = 'AlertCenter',
                subject = _cond,
                content = _cond_des 
                )
            sendemail.sendemail(sendemail.url,_pos_par)


class ConditionHandler(tornado.web.RequestHandler):
  
    #(r"/api/condition", ConditionHandler),
    def get(self):
        #get data 
        #warn_set
        coll = self.application.db.warn_set
        #elems_coll = coll.find({},{"condition_name" : 1,"_id" : 0})
        condition_list = coll.distinct('con_nam') 
        self.write(json.dumps(condition_list))
   
    def post(self):
        ''' 
          condition_name = con_nam
          condition_description = con_des
        '''
        _condition_name = self.get_argument('con_nam')
        _condition_description = self.get_argument('con_des')
        #test
        #print (_condition_name == u"")
        #print _condition_name
         #self.get_argument()
        _tem_dict = {}
        if _condition_name != u'':
            coll = self.application.db.warn_set    
            if coll.find({ 'con_nam' : _condition_name }) == None:
                _tem_dict['con_nam'] = _condition_name
                _tem_dict['con_des'] = _condition_description
                coll.insert(_tem_dict)
       

class ConditionPeopleHandler(tornado.web.RequestHandler):
    
    '''
        (r"/api/conditionpeople/source", ConditionPeopleHandler)
        use api /api/conditionpeople/source?condname=
    '''
    
    def get(self):
        
        _cond_name = self.get_argument('condname')
        _tem_people_dict = {}
        if _cond_name != u'':
            coll = self.application.db[_cond_name]
            for x in coll.find():
                _tem_people_dict[x[u'name']] = {
                    'name' : x['name'],
                    'email' : x['email'],
                    'mobi' : x['mobi']
                    }
                self.write(json.dumps(_tem_people_dict))

        #get condition people
        #pass   

    def post(self):
        
        #url
        _cond_name_set = self.get_argument('cond')
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


