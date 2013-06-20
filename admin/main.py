# coding=utf-8
from tornado.escape import url_unescape,utf8
import tornado.ioloop,tornado.web,tornado.httpserver,tornado.database,tornado.options

import datetime 
import random,string,json,urllib2,urllib,os
from jaccount import encrypt , decrypt , find , splitdata
import logging

from tornado.options import define,options
define("port", default=8000, help="run on the given port", type=int)

class BaseHandler(tornado.web.RequestHandler):
	def get_current_user(self):
		return self.get_secure_cookie("uid")

class adminHandler(BaseHandler):
	def get(self):
		if not self.current_user:
			try:
				if self.get_argument('login')=='1':
					self.render("login.html", notification = "密码错误")
			except:
				self.render("login.html", notification = "请输入用户名和密码")
		else:
			self.redirect("/admin/student")

# Student information query
class StudentHandler(BaseHandler):
	def get(self):
		if not self.current_user:
			self.redirect("/admin")
		else:
			info=[]
			if self.get_argument('op',None) and self.get_argument('q',None):
				option=self.get_argument('op',None)
				q=self.get_argument('q',None)
				info = self.query(option,q)
			chiname = self.get_secure_cookie("chiname")
			for item in info:
				print item
			self.render("admin_student.html", chiname=chiname , query_json=info)
			return

	def query(self,option,q):
		url_unescape(q,'utf-8')
		if(option == 'option1'):
			info = self.db.query('SELECT U.UID,U.USERNAME,U.CHINAME,D.DETECTTIME,D.STATUS FROM USER U,DETECT D \
								WHERE U.UID = D.OWNER AND U.CHINAME=\'%s\'' % (q))
		elif(option == 'option2'):
			info = self.db.query('SELECT U.UID,U.USERNAME,U.CHINAME,D.DETECTTIME,D.STATUS FROM USER U,DETECT D \
								WHERE U.UID = D.OWNER AND U.UID=%s' % (q))
		elif(option == 'option3'):
			pass
		# for item in info:
		# 	item['DETECTTIME'] = self.datetiem_handler(item['DETECTTIME'])
		return info
	
	def datetiem_handler(self,obj):
		if hasattr(obj, 'isoformat'):
			return obj.isoformat()
		elif isinstance(obj, None):
			return None
		else:
			raise TypeError, 'Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj))

	@property
	def db(self):
		return self.application.db
# jaccount login
class JaLoginHandler(BaseHandler):
	def get(self):
		if not self.get_arguments('jatkt'):
			siteID = 'jasignin20130507'
			uaBaseURL="http://jaccount.sjtu.edu.cn/jaccount/"
			returl = 'http://127.0.0.1:'+ port + '/admin/jalogin'
			iv = string.join(random.sample('1234567890abcdef',8),'')
			# print "iv:" , iv
			self.set_secure_cookie('iv' , iv , None)
			redirectURL =  uaBaseURL + "jalogin?sid="+siteID+"&returl="+encrypt(returl,iv)+"&se="+encrypt(iv,iv)
			self.redirect(redirectURL)
		else:
			try:
				if len(self.get_argument('jatkt')) == 0:
					raise tornado.web.HTTPError(404)
			except TypeError:
				raise tornado.web.HTTPError(404)
			iv = self.get_secure_cookie('iv')
			jatkt = self.get_argument('jatkt')
			data = decrypt(jatkt,iv)
			data = find(data,ur'ja[\s\S]*')
			url_unescape(data,'utf-8')
			ProfileData = splitdata(data)
			print data
			if self.checkUser(ProfileData['id']):
				self.set_secure_cookie('uid' , ProfileData['id'] , None)
				self.set_secure_cookie('chiname', ProfileData['chinesename'],None)
				self.set_cookie('login','0')
				if ProfileData['ja3rdpartySessionID'] != iv:
					self.write('Hacking Attempt~!')
					return
			else:
				self.set_cookie('login','1')
			self.redirect('/admin')

	def checkUser(self , uid):
		info = self.db.query('SELECT UID FROM USER WHERE UID = %s' % (uid))
		if info:
			return 1
		else: 
			return 0	

	@property
	def db(self):
		return self.application.db
# jaccount logout
class JaLogoutHandler(BaseHandler):
	def get(self):
		if self.current_user:
			siteID = 'jasignin20130507'
			uaBaseURL="http://jaccount.sjtu.edu.cn/jaccount/"
			returl = 'http://127.0.0.1:8000/admin'
			iv = self.get_secure_cookie('iv')
			redirectURL =  uaBaseURL + "ulogout?sid="+siteID+"&returl="+encrypt(returl,iv)
			self.clear_all_cookies()
			self.redirect(redirectURL)
		else:
			self.redirect('/admin')
"""
class JaLoginAPIHandler(BaseHandler):
	def post(self):
		decode_body = json.loads(self.request.body)
		username = decode_body['name']
 		password = decode_body['password']
		siteID = 'jasignin20130507'
		uaBaseURL="https://jaccount.sjtu.edu.cn/jaccount/"
		returl = 'http://127.0.0.1:8000/jastatus'
		iv = string.join(random.sample('1234567890abcdef',8),'')
		self.set_secure_cookie('iv' , iv , None)
		self.submit(username,password,siteID,uaBaseURL,returl,iv)

	def submit(self,name,password,siteID,uaBaseURL,returl,iv):
		values = {
				'name':name , 
				'pass':password , 
				'sid': siteID ,
				'returl':encrypt(returl,iv),
				'se':encrypt(iv,iv)
				}
		headers = {"Content-Type":"application/x-www-form-urlencoded",     
					"Connection":"Keep-Alive"
			}
		data = urllib.urlencode(values)
		req = urllib2.Request(uaBaseURL + 'ulogin', data,headers)
		response = urllib2.urlopen(req)
		print response.info(),response.read()
		return
		
class JaStatusAPIHandler(BaseHandler):
	def get(self):
		print "JaStatus"
		if not self.get_arguments('jatkt'):
			self.write({"error":1})
		else:
			try:
				if len(self.get_argument('jatkt')) == 0:
					raise tornado.web.HTTPError(404)
			except TypeError:
				raise tornado.web.HTTPError(404)
			iv = self.get_secure_cookie('iv')
			jatkt = self.get_argument('jatkt')
			data = decrypt(jatkt,iv)
			data = find(data,ur'ja[\s\S]*')
			data.decode('utf-8').encode('gbk')
			ProfileData = splitdata(data)
			print data.decode('utf-8').encode('gbk')
			self.set_secure_cookie('uid' , ProfileData['uid'] , None)
			self.set_secure_cookie('sessoinid' , ProfileData['ja3rdpartySessionID'] , None)
			if ProfileData['ja3rdpartySessionID'] != iv:
				self.write('Hacking Attempt~!')
			self.redirect('/')
"""
"""
管理界面学生信息查询api
"""
class adminSearchHandler(BaseHandler):
	def get(self):
		option = self.get_argument('op')
		q = self.get_argument('q')
		info = self.query(option,q)
		self.write(info)
		return

	def datetiem_handler(self,obj):
		if hasattr(obj, 'isoformat'):
			return obj.isoformat()
		elif isinstance(obj, None):
			return None
		else:
			raise TypeError, 'Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj))

	def query(self,option,q):
		url_unescape(q,'utf-8')
		if(option == 'option1'):
			info = self.db.query('SELECT U.UID,U.USERNAME,U.CHINAME,D.DETECTTIME,D.STATUS FROM USER U,DETECT D \
								WHERE U.UID = D.OWNER AND U.CHINAME=\'%s\'' % (q))
		elif(option == 'option2'):
			info = self.db.query('SELECT U.UID,U.USERNAME,U.CHINAME,D.DETECTTIME,D.STATUS FROM USER U,DETECT D \
								WHERE U.UID = D.OWNER AND U.UID=%s' % (q))
		elif(option == 'option3'):
			pass
		for item in info:
			item['DETECTTIME'] = self.datetiem_handler(item['DETECTTIME'])
			# item['CHINAME'] = utf8(item['CHINAME'])
		return json.dumps(info)

	@property
	def db(self):
		return self.application.db

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r"/admin", adminHandler),
			(r"/admin/jalogin" , JaLoginHandler),
			(r"/admin/logout" , JaLogoutHandler),
			(r"/admin/search", adminSearchHandler),
			(r"/admin/student", StudentHandler),
			# (r"/admin/index" , adminIndexHandler)
			# (r"/jalogin", JaLoginAPIHandler),
			# (r"/jastatus", JaStatusAPIHandler),
		]
		settings = dict(
			debug = True,
			login_url = "/login",
			template_path = os.path.join(os.path.dirname(__file__), "templates").encode("gbk"), 
			static_path = os.path.join(os.path.dirname(__file__), 'static').encode("gbk"),
			cookie_secret = "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E="
		)
		tornado.web.Application.__init__(self , handlers , **settings)
		self.db = tornado.database.Connection(host = 'localhost:3306' , database= 'mobile' , user = 'root' , password = '')

if __name__ == "__main__":
	print "Welcome to Mobile Checkin Server"
	# tornado.options.parse_config_file("config.conf")
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()