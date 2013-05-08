# coding=gbk
# $File: sv.py
# $Date: Fri Apr 26 14:14:27 2013 +0800
# $Author: ronnie.alonso@gmail.com
#
#      0. You just DO WHAT THE FUCK YOU WANT TO.
import tornado.web
import tornado.httpclient
import os,json,string
from datetime import *
from ctypes import cdll, c_int , c_char_p , c_double
from basic import BaseHandler

# Speech Verify Engine initialize
sv_dll = cdll.LoadLibrary("./sv/libsv.so")
sv_dll.SVtrain.argtypes = [c_char_p , c_char_p , c_char_p , c_char_p , c_char_p]
sv_dll.SVdetect.argtypes = [c_char_p , c_char_p , c_char_p , c_double , c_int]


"""speech train API
API http://localhost:8000/svtrain
POST:	http://localhost:8000/svtrain
		{"voice1":voice
		"voice2":voice
		"voice3":voice
		}
HEADER:  {  "Accept":"application/json",
			"Connection": "Keep-Alive", 
			"Cache-Control": "no-cache" ,
			"Cookie": client_cookie}
RESPONSE:{  "error":}
error:	0 for success
		1 for not login
		2:newSVEngine error
		3:speaker adapt basic failed
		-1 for failure in train
"""
class SpeechTrainHandler(BaseHandler):
	def post(self):
		if not self.current_user:
			self.write({"error":1})
			return

		tmp_uid = self.current_user
		# upload file
		uploadfile = self.request.files.get('voice1')
		file1 = self.handle_filename(tmp_uid , uploadfile[0]['filename'] , 'audio/')
		picfile = open(file1,"wb")
		picfile.write(uploadfile[0]['body'])
		picfile.close()

		uploadfile = self.request.files.get('voice2')
		file2 = self.handle_filename(tmp_uid , uploadfile[0]['filename'] , 'audio/')
		picfile = open(file2,"wb")
		picfile.write(uploadfile[0]['body'])
		picfile.close()

		uploadfile = self.request.files.get('voice3')
		file3 = self.handle_filename(tmp_uid , uploadfile[0]['filename'] , 'audio/')
		picfile = open(file3,"wb")
		picfile.write(uploadfile[0]['body'])
		picfile.close()

		try:
			ret = sv_dll.SVtrain("./sv/sv.0.0.3.2.bin" , "./static/audio_mod/%s.bin" % (tmp_uid) , "./"+file1 , "./"+file2 , "./"+file3)
			print ret
			if (ret == 1):
				self.write({"error": 2})
				return
			elif (ret ==2):
				self.write({"error": 3})
				return
		except:
			self.write({"error": -1})
			return

		now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		self.db.execute('UPDATE USER SET AUDIOENGINE = \'%s.bin\' WHERE UID = %s;' % (tmp_uid , tmp_uid))
		self.db.execute('INSERT INTO AUDIO(OWNER,AUDIOHASH,CREATETIME) VALUES(\'%s\',\'%s\',\'%s\');' % (tmp_uid , file1 ,now))
		self.db.execute('INSERT INTO AUDIO(OWNER,AUDIOHASH,CREATETIME) VALUES(\'%s\',\'%s\',\'%s\');' % (tmp_uid , file2 ,now))
		self.db.execute('INSERT INTO AUDIO(OWNER,AUDIOHASH,CREATETIME) VALUES(\'%s\',\'%s\',\'%s\');' % (tmp_uid , file3 ,now))
		self.write({"error": 0})

	@property
	def db(self):
		return self.application.db

"""speech detect API
API http://localhost:8000/svdetect
POST:	http://localhost:8000/svdetect
		{"voice":voice}
HEADER:  {  "Accept":"application/json",
			"Connection": "Keep-Alive", 
			"Cache-Control": "no-cache" ,
			"Cookie": client_cookie}
RESPONSE:{  "error":}
error:	0 for success
		1 for not login
		2 for not accepted
		4 for user not initialize audio
		5 for no sessionid
		-1 for failure in detect process
"""
class SpeechDetectHandler(BaseHandler):
	def post(self):
		if not self.current_user:
			self.write({"error":1})
			return
		tmp_uid = self.current_user
		if (not self.get_sessionid()):
			self.write({"error":5})
			return
		sessionid = int(self.get_sessionid())

		uploadfile = self.request.files.get('voice')
		tmp_path = self.handle_filename(tmp_uid , uploadfile[0]['filename'] , 'audio/')
		picfile = open(tmp_path,"wb")
		picfile.write(uploadfile[0]['body'])
		picfile.close()

		query = self.db.query("SELECT AUDIOENGINE FROM USER WHERE UID = %s" % (tmp_uid))
		if not query:
			self.write({"error":4})
			return

		try:
			ret = sv_dll.SVdetect("./sv/sv.0.0.3.2.bin" , "./static/audio_mod/%s.bin" % (tmp_uid) , "./"+tmp_path , 1 ,1)
			if (ret == 1):
				self.db.execute('UPDATE DETECT SET AUDIOHASH = \'%s\', AUDIODETECT = %d WHERE SESSIONID=%d;' % 
		(tmp_path ,0,sessionid))
				self.write({"error": 0})
				return
			else:
				self.db.execute('UPDATE DETECT SET AUDIOHASH = \'%s\' , AUDIODETECT = %d WHERE SESSIONID=%d;' % 
		(tmp_path ,1,sessionid))
				self.write({"error":2})
				return
		except:
			self.write({"error": -1})
			return

	@property
	def db(self):
		return self.application.db