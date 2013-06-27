# coding=gbk
# $File: face.py
# $Date: Sun Feb 24 14:47:27 2013 +0800
# $Author: ronnie.alonso@gmail.com
#
#      0. You just DO WHAT THE FUCK YOU WANT TO.
import tornado.web
import tornado.httpclient
import os,json,string
from datetime import datetime
from basic import BaseHandler
from facepp import API,APIError,Img

API_KEY = 'b3b9061aaf64ea2515a3538dfb624e94'
API_SECRET = 'OfvW6DdyM9iqAa8TkBoBhoiWANX6Kn2Z'
api = API(API_KEY, API_SECRET)

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
	# @tornado.web.asynchronous
	def post(self):
		if not self.current_user:
			self.write({"error":2})
			return
		if (not self.get_secure_cookie("sessionid")):
			self.write({"error":4})
			return
		sessionid = int(self.get_sessionid())
		tmp_uid = self.current_user

		uploadfile = self.request.files.get('pic')
		img_binary = uploadfile[0]['body']
		img_name = uploadfile[0]['filename']
		tmp_path = self.handle_filename(tmp_uid , img_name , 'img/')
		picfile = open(tmp_path,"wb")
		picfile.write(img_binary)
		picfile.close()

		try:
			face_detect = api.detection.detect(img = Img(img_binary,img_name))
			if not face_detect['face']:
				self.write({'error':3 , 'info':'NO FACE'})
				return
			else:
				tmp_face1 = face_detect['face'][0]['face_id']
		except APIError,e:
			self.write({'error':1 , 'info':json.loads(e.body)['error']})
			return

		info = self.db.query('SELECT IMAGESAMPLE FROM USER WHERE UID = %d' % (string.atoi(tmp_uid)))
		tmp_face2 = info[0]['IMAGESAMPLE']

		# global API_SECRET,API_KEY
		# client = tornado.httpclient.AsyncHTTPClient()
		# client.fetch("https://api.faceplusplus.com/recognition/compare?api_secret=%s&api_key=%s&face_id2=%s&face_id1=%s"
		# 			% (API_KEY,API_SECRET,tmp_face1,tmp_face2),
		# 			callback=self.on_response)
		response = api.recognition.compare(face_id1 = tmp_face1 , face_id2 =tmp_face2)
		similarity = float(response["similarity"])
		self.db.execute('UPDATE DETECT SET FACEHASH=\'%s\' , FACEDETECT=%f WHERE SESSIONID=%d;' % 
		(tmp_face1 , similarity , sessionid))
		self.write({"error":0,
					"similarity":similarity})

		
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
	# @tornado.web.asynchronous
	def post(self):
		if not self.current_user:
			self.write({"error":2})
			return
		query = self.db.execute("SELECT IMAGESAMPLE FROM USER WHERE UID = %s" % (self.current_user))
		if query:
			self.write({"error":4})
			return

		tmp_uid = self.current_user
		uploadfile = self.request.files.get('pic')
		img_binary = uploadfile[0]['body']
		img_name = uploadfile[0]['filename']
		tmp_path = self.handle_filename(tmp_uid , img_name , 'img/')

		picfile = open(tmp_path,"wb")
		picfile.write(img_binary)
		picfile.close()

		try:
			face_detect = api.detection.detect(img = Img(img_binary,img_name))
			if not face_detect['face']:
				self.write({'error':5,'info':'No face is detected'})
				return
			else:
				tmp_face1 = face_detect['face'][0]['face_id']
		except APIError,e:
			self.write({'error':1 , 'info':json.loads(e.body)['error']})
			return
		add_face = api.person.add_face(person_name = tmp_uid,face_id = tmp_face1)
		if add_face["success"] == True:
			self.db.execute("UPDATE USER SET IMAGESAMPLE = \'%s\'	WHERE UID = %s" % (tmp_face1 , tmp_uid))
			self.write({"error":0,"faceid":tmp_face1})
		else:
			self.write({"error":3})

