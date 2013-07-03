# coding=gbk
# $File: basic.py
# $Date: Sun Feb 24 14:47:27 2013 +0800
# $Author: ronnie.alonso@gmail.com
#
#	  0. You just DO WHAT THE FUCK YOU WANT TO.
import tornado.web
import os,json,sys
from datetime import *
import tornado.httpclient
from gps import spherical_distance

class BaseHandler(tornado.web.RequestHandler):
	def get_current_user(self):
		return self.get_secure_cookie("uid")
	def get_sessionid(self):
		return self.get_secure_cookie('sessionid')

	def handle_filename(self , uid , filename , loc): # loc = "img/" or "audio/"
		format = filename.rsplit('.' , 1)
		s = datetime.now()
		try:
			path = 'static/'+ loc + uid + "%d%d%d%d."%(s.hour,s.minute,s.second,s.microsecond) + format[1]
		except:
			path = 'static/' + loc + uid + "%d%d%d%d"%(s.hour,s.minute,s.second,s.microsecond)
		# unicode error
		return path.encode('gbk')

	@property
	def db(self):
		return self.application.db

"""登陆界面
API:	http://domain:port/login
POST:	{'name':'xxx','password':'xxx'}
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

"""用户注册
API:	http://domain:port/login
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
			# try:
			#	 person_create = api.person.create(person_id = res , group_name = u'Students')
			# except APIError,e:
			#	 self.write({'error':3 , 'info':json.loads(e.body)['error']})
			#	 return
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

"""check user status
API:	
GET: http://domain:port/checkstatus
HEADER:  {  "Content-type":"application/json",
			"Accept":"text/plain",
			"Connection": "Keep-Alive", 
			"Cache-Control": "no-cache",
			"Cookie": client_cookie }
RESPONSE:{  "error":0}
error:  0 for success
		1 for not login
		2 for SQL error
"""
class CheckStatusHandler(BaseHandler):
	def get(self):
		if not self.current_user:
			self.write({"error":2})
			return
		uid = self.current_user
		try:
			info = self.db.query('SELECT IMAGESAMPLE,AUDIOENGINE,LOCID FROM USER WHERE UID = %s;' % (uid))
			res = info[0]
			res['error'] = 0
			self.write(res)
			return
		except:
			self.write({"error":2})
			return 

"""DetectCreate API
API http://domain:port/detectcreate
POST:   http://domain:port/detectcreate
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

"""DetectResult API
API http://domain:port/getdetectresult
POST:   http://domain:port/getdetectresult
HEADER:  {  "Accept":"application/json",
			"Connection": "Keep-Alive", 
			"Cache-Control": "no-cache" ,
			"Cookie": client_cookie}
RESPONSE:{  "error": 0}
error:  0 for success
		1 for fail
		2 for not login
		3 for no sessionid
		4 for empty SQL result
		5 for SQL error
	6 for not enough detect info
"""
class DetectResultHandler(BaseHandler):
	def post(self):
		if (not self.current_user):
			self.write({"error":2})
			return
		if (not self.get_sessionid()):
			self.write({"error":3})
			return
		uid = self.current_user
		sessionid = self.get_secure_cookie("sessionid")
		result = self.evaluation(uid,sessionid)
		self.write({"error":result})
			
		
	def evaluation(self , uid , sessionid):
		info = self.db.query('SELECT FACEDETECT,AUDIODETECT,LATITUDE,LONGITUDE,DETECTTIME FROM DETECT WHERE OWNER = %s AND SESSIONID = %s;' % 
			(uid , sessionid))
		if (not info):
			return 4

		info = info[0]
		timedetect =  info['DETECTTIME']
		facedetect = info['FACEDETECT']
		audiodetect = info['AUDIODETECT']
		loc_detect = [info['LATITUDE'] , info['LONGITUDE']]
		if (facedetect == None) or (audiodetect==None) or (loc_detect==None):
			return 6

		info = self.db.query('SELECT * FROM LOCATION L,USER U WHERE L.LOCID = U.LOCID AND U.UID = %s;' % (uid))
		if (not info):
			return 4
		info = info[0]
		loc_init = [info['LATITUDE'],info['LONGITUDE']]
		loc_name = info['LOCATIONNAME']
		starttime = info['STARTTIME']
		termitime = info['TERMITIME']

		dis = spherical_distance(loc_detect , loc_init)
		tim = starttime <= timedetect and timedetect <= termitime
		
		if (dis <= 4) and (facedetect >= 60) and (audiodetect > 0.6) and (tim):
			detect_status=0
		else:
			detect_status=1

		try:
			sql = "UPDATE DETECT SET STATUS=%d WHERE OWNER = %s AND SESSIONID = %s;"\
			 % (detect_status,uid,sessionid)
			info=self.db.execute(sql)
		except:
			return 5

		return detect_status

