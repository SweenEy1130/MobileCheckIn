# coding=gbk
# $File: basic.py
# $Date: Sun Feb 24 14:47:27 2013 +0800
# $Author: ronnie.alonso@gmail.com
#
#      0. You just DO WHAT THE FUCK YOU WANT TO.
import tornado.web
import os,json,sys
from facepp import API,File,APIError
from datetime import *
import tornado.httpclient
from gps import spherical_distance

API_KEY = 'b3b9061aaf64ea2515a3538dfb624e94'
API_SECRET = 'OfvW6DdyM9iqAa8TkBoBhoiWANX6Kn2Z'
api = API(API_KEY, API_SECRET)

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("uid")

    def get_sessionid(self):
        return self.get_secure_cookie("sessionid")

    def handle_filename(self , uid , filename , loc): # loc = "img/" or "audio/"
        format = filename.rsplit('.' , 1)
        s = datetime.now()
        try:
            path = 'static/'+ loc + uid + "%d%d%d%d."%(s.hour,s.minute,s.second,s.microsecond) + format[1]
        except:
            path = 'static/' + loc + uid + "%d%d%d%d"%(s.hour,s.minute,s.second,s.microsecond)
        # unicode error
        return path.encode('gbk')

class TestHandler(BaseHandler):
    def get(self):
        self.write("GET method")

    def post(self):
        print self.request
        self.write("POST method")

"""登陆界面
API:    http://localhost:8000/login
POST:    {'name':'xxx','password':'xxx'}
HEADER:  {  "Content-type":"application/json",
            "Accept":"text/plain",
            "Connection": "Keep-Alive", 
            "Cache-Control": "no-cache" }
RESPONSE:{  "error":0}
error:  0 for success
        1 for invalid password
        2 for password or username can't be empty
"""
class LoginHandler(BaseHandler):
    def post(self):
        try:
            decode_body = json.loads(self.request.body)
            username = decode_body['name']
            password = decode_body['password']
        except:
            self.write({'error':2})
            return
        if (not username) or (not password):
            # password or username can't be empty
            self.write({'error':2})
            return

        uid = self.checkUser(username , password)
        if uid != -1:
            self.set_secure_cookie("uid", str(uid), 1)
            self.write({'error':0})
        else:
            # invalid password
            self.write({'error':1})

    def checkUser(self , username , password):
        info = self.db.query('SELECT PASSWORD,UID FROM USER WHERE USERNAME = \'%s\'' % (username))
        if info:
            t_pass = info[0]['PASSWORD']
            t_uid = info[0]['UID']
            if t_pass == password:
                return t_uid
            else: return -1
        else: return -1

    @property
    def db(self):
        return self.application.db

"""用户注册
API:    http://localhost:8000/login
POST   {'name':'xxx','password':'xxx'}
HEADER {"Content-type":"application/json",
        "Accept":"text/plain",
        "Connection": "Keep-Alive", 
        "Cache-Control": "no-cache" }
RESPONSE:{  "error":}
error:  0 for success
        1 for username exist
        2 for password or username can't be empty
        3 for FACEPP API Error
        4 for SQL Error
"""
class RegisterHandler(BaseHandler):
    def post(self):
        try:
            decode_body = json.loads(self.request.body)
            username = decode_body['name']
            password = decode_body['password']
        except:
            self.write({'error':2})
            return
        if (not username) or (not password):
            # password or username can't be empty
            self.write({'error':2})
            return

        try:
            res = self.insertInfo(username , password)
        except:
            self.wirte({'error':4})
            return

        if res == -1:
            # user exist
            self.write({'error':1})
        else:
            # register success
            self.set_secure_cookie("uid", str(res), 1)
            try:
                person_create = api.person.create(person_name = res , group_name = u'Students')
            except APIError,e:
                self.write({'error':3 , 'info':json.loads(e.body)['error']})
                return
            self.write({'error':0})

    def insertInfo(self , username , password):
        find = self.db.query('SELECT UID FROM USER WHERE USERNAME = \'%s\'' % (username))
        if find:
            return -1
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.db.execute('INSERT INTO USER(USERNAME,PASSWORD,CREATETIME) VALUES(\'%s\',\'%s\',\'%s\');' % 
            (username , password ,now))
        info = self.db.query('SELECT UID FROM USER WHERE USERNAME = \'%s\'' % (username))
        uid = info[0]['UID']
        return uid

    @property
    def db(self):
        return self.application.db

"""DetectCreate API
API http://localhost:8000/detectcreate
POST:   http://localhost:8000/detectcreate
HEADER:  {  "Accept":"application/json",
            "Connection": "Keep-Alive", 
            "Cache-Control": "no-cache" ,
            "Cookie": client_cookie}
RESPONSE:{  "error": }
error:  0 for success
        1 for SQL error
        2 for not login
return_cookies will have an ||sessionid|| to detect
"""
class DetectCreateHandler(BaseHandler):
    def post(self):
        if not self.current_user:
            self.write({"error":2})
            return
        uid = self.current_user
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            self.db.execute('INSERT INTO DETECT(OWNER,DETECTTIME) VALUES(\'%s\',\'%s\');' % 
                (uid ,now))
            info = self.db.query('SELECT SESSIONID FROM DETECT WHERE OWNER = \'%s\' AND DETECTTIME = \'%s\'' % 
              (uid , now))
            sessionid = info[0]['SESSIONID']
        except e:
            self.write({"error":1})
            return
        self.set_secure_cookie("sessionid", str(sessionid), 1)
        self.write({"error":0})
        return

    @property
    def db(self):
        return self.application.db


"""DetectResult API
API http://localhost:8000/getdetectresult
POST:   http://localhost:8000/getdetectresult
HEADER:  {  "Accept":"application/json",
            "Connection": "Keep-Alive", 
            "Cache-Control": "no-cache" ,
            "Cookie": client_cookie}
RESPONSE:{  "error": 0}
error:  0 for success
        1 for fail
        2 for not login
        3 for no sessionid
        4 for SQL error
"""
class DetectResultHandler(BaseHandler):
    def post(self):
        if (not self.current_user):
            self.write({"error":2})
            return
        if (not self.get_sessionid()):
            self.write({"error":3})
            return
        uid = int(self.current_user)
        sessionid = int(self.get_sessionid())
        
        result = self.evaluation(uid,sessionid)
        return
            
        
    def evaluation(self , uid , sessionid):
        info = self.db.query('SELECT FACEDETECT,AUDIODETECT,LATITUDE,LONGITUDE FROM DETECT WHERE OWNER = %s AND SESSIONID = %d' % 
            (uid , sessionid))
        if (not info):
            self.write({"error":4})
            return 0
        info = info[0]
        facedetect = info['FACEDETECT']
        audiodetect = info['AUDIODETECT']
        loc_detect = [info['LATITUDE'] , info['LONGITUDE']]
        info = self.db.query('SELECT L.LOCATIONNAME, L.LONGITUDE, L.LATITUDE FROM LOCATION L,USER U WHERE L.LOCID = U.LOCID AND U.UID = %d' %
            (uid))
        if (not info):
            self.write({"error":4})
            return 0
        info = info[0]
        loc_init = [info['LATITUDE'],info['LONGITUDE']]
        loc_name = info['LOCATIONNAME']
        dis = spherical_distance(loc_detect , loc_init)
        if (dis <= 4) and (facedetect >= 70) and (audiodetet == 0):
            self.write({"error":0})
            return 1
        else:
            self.write({'error':1})

    @property
    def db(self):
        return self.application.db

