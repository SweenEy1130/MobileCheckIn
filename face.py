# coding=gbk
# $File: face.py
# $Date: Sun Feb 24 14:47:27 2013 +0800
# $Author: ronnie.alonso@gmail.com
#
#      0. You just DO WHAT THE FUCK YOU WANT TO.
import tornado.web
import tornado.httpclient
import os,json,string
import faceppKit
from datetime import datetime
from basic import BaseHandler

"""face verification API
API http://localhost:8000/faceverify
POST:	http://localhost:8000/faceverify
		{"pic":picture_file}
HEADER:  {  "Accept":"application/json",
			"Connection": "Keep-Alive", 
			"Cache-Control": "no-cache" ,
			"Cookie": client_cookie}
RESPONSE:{  "error":
			"similarity":}
error:	0 for success
		1 for FACEPP APIError
		2 for not login
		3 for not face
		4 for no sessionid
Cookie should contain the response set-cookie from the sever when user login(important!)
example:	HTTP Request HEADER		
			{"Accept":"application/json",
			"Connection": "Keep-Alive", 
			"Cache-Control": "no-cache",
			"Cookie": client_cookie }
"""
class FaceppHandler(BaseHandler):
	def handle_request(self,response):
		if response.error:
			print 'error:1;info:'+response.error
			self.write({'error':1,'info':response.error})
			self.finish()
			return
		else:
			face_detect = json.loads(response.body)
			if not face_detect['face']:
				print 'error:3;info:NO FACE'
				self.write({'error':3 , 'info':'NO FACE'})
				self.finish()
				return
			else:
				tmp_face1 = face_detect['face'][0]['face_id']

			info = self.db.query('SELECT IMAGESAMPLE FROM USER WHERE UID = %d' % (string.atoi(self.uid)))
			tmp_face2 = info[0]['IMAGESAMPLE']

			http_client = tornado.httpclient.AsyncHTTPClient()
			http_request=faceppKit.FaceCompare(tmp_face1,tmp_face2)
			http_client.fetch(http_request, callback=self.handle_request2)

	def handle_request2(self,response):
		response=json.loads(response.body)
		if response.has_key("similarity"):
			similarity = float(response["similarity"])
			self.db.execute('UPDATE DETECT SET FACEHASH=\'%s\' , FACEDETECT=%f WHERE SESSIONID=%d;' % (self.filename , similarity , self.sessionid))
			print 'error:0;	similarity:	%f' % similarity			
			self.write({"error":0,"similarity":similarity})
		else:
			print 'error:3;info:no similarity'
			self.write({"error":1})
		self.finish() 

	@tornado.web.asynchronous
	def post(self):
		if not self.current_user:
			print 'error:2;info:not login'
			self.write({"error":2})
			self.finish()
			return
		if (not self.get_secure_cookie("sessionid")):
			print 'error:4;info:not create'
			self.write({"error":4})
			self.finish()
			return
		self.sessionid = int(self.get_sessionid())
		self.uid = self.current_user

		uploadfile = self.request.files.get('pic')
		img_binary = uploadfile[0]['body']
		img_name = uploadfile[0]['filename'].encode('gbk')
		tmp_path = self.handle_filename(self.uid , img_name , 'img/')
		self.filename = tmp_path.split('/')[2]
		picfile = open(tmp_path,"wb")
		picfile.write(img_binary)
		picfile.close()

		http_client = tornado.httpclient.AsyncHTTPClient()
		http_request=faceppKit.FaceDetect(img_binary,img_name)
		http_client.fetch(http_request, callback=self.handle_request)

"""face regeister API
API http://localhost:8000/faceregister
POST:	http://localhost:8000/faceregister
		{"pic":picture_file}
HEADER:  {  "Accept":"application/json",
			"Connection": "Keep-Alive", 
			"Cache-Control": "no-cache" ,
			"Cookie": client_cookie}
RESPONSE:{  "error":
			"faceid":}

error:	0 for success
		1 for face unrecogized
		2 for not login
		3 for face_add error
		4 for already register
Cookie should contain the response set-cookie from the sever when user login(important!)
the client_cookie can get from the server's response
example:	HTTP Request HEADER		
			{"Content-type":"image/jpeg",
			"Accept":"application/json",
			"Connection": "Keep-Alive", 
			"Cache-Control": "no-cache" ,
			"Cookie": client_cookie}
"""
class FaceRegisterHandler(BaseHandler):
	def handle_request(self,response):
		if response.error:
			print 'error:1;info:'+response.error
			self.write({'error':1,'info':response.error})
			self.finish()
			return
		else:
			face_detect = json.loads(response.body)
			if not face_detect['face']:
				print 'error:5;info:No face is detected'
				self.write({'error':5,'info':'No face is detected'})
				self.finish()
				return
			else:
				self.tmp_face1 = face_detect['face'][0]['face_id']

		http_client = tornado.httpclient.AsyncHTTPClient()
		http_request=faceppKit.AddFace(self.uid,self.tmp_face1)
		http_client.fetch(http_request, callback=self.handle_request2)

	def handle_request2(self,response):
		add_face=json.loads(response.body)
		if add_face["success"] == True:
			self.db.execute("UPDATE USER SET IMAGESAMPLE = \'%s\' WHERE UID = %s" % (self.tmp_face1 , self.uid))
			self.write({"error":0,"faceid":self.tmp_face1})
		else:
			self.write({"error":3})
		self.finish()

	@tornado.web.asynchronous
	def post(self):
		if not self.current_user:
			self.write({"error":2})
			self.finish()
			return
		query = self.db.execute("SELECT IMAGESAMPLE FROM USER WHERE UID = %s" % (self.current_user))
		if query:
			self.write({"error":4})
			self.finish()
			return
		self.uid = self.current_user
		uploadfile = self.request.files.get('pic')

		img_binary = uploadfile[0]['body']
		img_name = uploadfile[0]['filename'].encode('gbk')
		tmp_path = self.handle_filename(self.uid , img_name , 'img/')
		picfile = open(tmp_path,"wb")
		picfile.write(img_binary)
		picfile.close()

		http_client = tornado.httpclient.AsyncHTTPClient()
		http_request=faceppKit.FaceDetect(img_binary,img_name)
		http_client.fetch(http_request, callback=self.handle_request)

