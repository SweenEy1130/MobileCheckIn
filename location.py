# coding=gbk
# $File: location.py
# $Date: Fri Mar 2 1:09:27 2013 +0800
# $Author: ronnie.alonso@gmail.com
#
#      0. You just DO WHAT THE FUCK YOU WANT TO. 
import tornado.web
import tornado.httpclient
import os,json,string
from datetime import *
from basic import BaseHandler

"""Upload Location API
API http://localhost:8000/uploadlocation
POST:   http://localhost:8000/uploadlocation
	{
		'latitude':latitude,
		'longitude':longitude
	}
HEADER:  {  "Accept":"application/json",
            "Connection": "Keep-Alive", 
            "Cache-Control": "no-cache" ,
            "Cookie": client_cookie
            }
RESPONSE:{  "error":0}
error:  0 for success
        1 for not login
        2 for no longitude or latitude
        3 for no sessionid
"""
class UploadLocationHandler(BaseHandler):
	def post(self):
		if not self.current_user:
			self.write({"error":1})
			return
		if (not self.get_sessionid()):
			self.write({"error":3})
			return
		sessionid = int(self.get_sessionid())
		try:
			decode_body = json.loads(self.request.body)
			longitude = float(decode_body['longitude'])
			latitude = float(decode_body['latitude'])
		except:
			self.write({'error':2})
			return
		# print latitude,longitude
		self.db.execute('UPDATE DETECT SET LATITUDE=%f , LONGITUDE=%f WHERE SESSIONID = %d;' % 
		(latitude ,longitude , sessionid))
		self.write({'error':0})
		return

"""LocationRegisterHandler API
API http://localhost:8000/registerlocation
POST:   http://localhost:8000/registerlocation
	{
		'locid':1 //1 for SJTU
	}
HEADER:  {  "Accept":"application/json",
            "Connection": "Keep-Alive", 
            "Cache-Control": "no-cache" ,
            "Cookie": client_cookie}
"""
class LocationRegisterHandler(BaseHandler):
	def post(self):
		if not self.current_user:
			self.write({"error":1})
			return
		decode_body = json.loads(self.request.body)
		locid = decode_body['locid']
		uid = self.current_user

		self.db.execute('UPDATE USER SET LOCID = %d WHERE UID = %s;' % (locid , uid))
		self.write({'error':0})