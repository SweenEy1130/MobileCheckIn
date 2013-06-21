#coding=utf-8
# jaccount login
class JaLoginHandler(BaseHandler):
	def get(self):
		if not self.get_arguments('jatkt'):
			siteID = 'jasignin20130507'
			uaBaseURL="http://jaccount.sjtu.edu.cn/jaccount/"
			returl = 'http://127.0.0.1:8000/admin/jalogin'
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
			# utf-8编码
			data.decode('utf-8')
			ProfileData = splitdata(data)
			if self.checkUser(ProfileData):
				self.set_secure_cookie('uid' , ProfileData['id'] , None)
				self.set_secure_cookie('chiname', ProfileData['chinesename'],None)
				self.set_cookie('login','0')
				if ProfileData['ja3rdpartySessionID'] != iv:
					self.write('Hacking Attempt~!')
					return
			else:
				self.set_cookie('login','1')
			self.redirect('/admin')

	def checkUser(self , profile):
		uid = profile['id']
		info = self.db.query('SELECT UID,CHINAME,USERNAME,DEPARTMENT FROM USER WHERE UID = %s;' % (uid))
		if info:
			if(not info[0]['CHINAME'] or not info[0]['DEPARTMENT']):
				sql = 'UPDATE USER SET CHINAME=\'%s\',DEPARTMENT=\'%s\' WHERE UID = %s;' \
										% (profile['chinesename'],profile['dept'],uid)
				res = self.db.execute(sql)
			return 1
		else: 
			sql = 'INSERT INTO USER(UID,CHINAME,USERNAME,DEPARTMENT,PASSWORD)\
						 VALUES (%s,\'%s\',%s,\'%s\','123456');' %\
						 (profile['id'],profile['chinesename'],profile['uid'],profile['dept'])
			res = self.db.execute(sql)
			return 0	

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
		self.redirect('/admin')