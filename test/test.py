# coding=gbk
# $File: api_test.py
# $Date: Sun Feb 24 14:47:27 2013 +0800
# $Author: ronnie.alonso@gmail.com
#
#      0. You just DO WHAT THE FUCK YOU WANT TO. 
import httplib, urllib, urllib2
import json,string
import requests
import sys,json
from facepp import API,File,APIError
API_KEY = 'b3b9061aaf64ea2515a3538dfb624e94'
API_SECRET = 'OfvW6DdyM9iqAa8TkBoBhoiWANX6Kn2Z'
api = API(API_KEY, API_SECRET)

def test():
	# GET
	conn = httplib.HTTPConnection("127.0.0.1:8000")
	conn.request("GET","/test")
	r1 = conn.getresponse()
	print r1.read()
	conn.close()

def test_checkstatus():
	#GET
	global client_cookie
	headers = {"Content-type":"application/json",
				"Accept":"text/plain",
				"Connection": "Keep-Alive", 
				"Cache-Control": "no-cache" ,
				"Cookie": client_cookie}
	conn = httplib.HTTPConnection("127.0.0.1:8000")
	conn.request("GET","/checkstatus", body = '' , headers = headers)
	r1 = conn.getresponse()
	print "Check Status:"
	print r1.read()
	conn.close()

def test_login(username,password):
	# POST
	params = json.dumps({'name':username , 'password':password})
	headers = {"Content-type":"application/json",
				"Accept":"text/plain",
				"Connection": "Keep-Alive", 
				"Cache-Control": "no-cache" }
	conn = httplib.HTTPConnection("127.0.0.1:8000")
	conn.request("POST","/login",params,headers)
	r1 = conn.getresponse()
	print "User login:"
	print r1.read()
	global client_cookie
	client_cookie = r1.getheader('set-cookie')
	conn.close()

def test_register(username,password):
	# POST
	params = json.dumps({'name':username , 'password':password})
	headers = {"Content-type":"application/json",
				"Accept":"text/plain",
				"Connection": "Keep-Alive", 
				"Cache-Control": "no-cache" }
	conn = httplib.HTTPConnection("127.0.0.1:8000")
	conn.request("POST","/register",params,headers)
	r1 = conn.getresponse()
	print "User register:"
	print r1.read()
	global client_cookie
	client_cookie = r1.getheader('set-cookie')
	conn.close()

def test_faceregister(filename):
	global client_cookie
	tmp_path = filename.encode('gbk')
	url = "http://127.0.0.1:8000/faceregister"
	files = {'pic': (filename, open(tmp_path, 'rb'))}
	headers = {	"Accept":"application/json",
            	"Connection": "Keep-Alive", 
            	"Cache-Control": "no-cache" ,
            	"Cookie": client_cookie}
	r = requests.post(url, headers=headers , files=files)
	print "Face register:\n" , r.text

def test_faceverify(filename):
	global client_cookie
	tmp_path = filename.encode('gbk')
	url = "http://127.0.0.1:8000/faceverify"
	files = {'pic': (filename, open(tmp_path, 'rb'))}
	headers = {	"Accept":"application/json",
            	"Connection": "Keep-Alive", 
            	"Cache-Control": "no-cache" ,
            	"Cookie": client_cookie}
	r = requests.post(url, headers=headers , files=files)
	print "Face verify:\n" , r.text

def test_svtrain(filename1 , filename2 ,filename3):
	global client_cookie
	file1 = filename1.encode('gbk')
	file2 = filename2.encode('gbk')
	file3 = filename3.encode('gbk')
	url = "http://127.0.0.1:8000/svtrain"
	files = {'voice1': (filename1, open(file1, 'rb')),
			'voice2': (filename2, open(file2, 'rb')),
			'voice3': (filename3, open(file3, 'rb'))
			}
	headers = {	"Accept":"application/json",
            	"Connection": "Keep-Alive", 
            	"Cache-Control": "no-cache" ,
            	"Cookie": client_cookie}
	r = requests.post(url , headers = headers , files = files)
	print "SV train:\n", r.text

def test_svdetect(filename):
	global client_cookie
	tmp_path = filename.encode('gbk')
	url = "http://127.0.0.1:8000/svdetect"
	files = {'voice': (filename, open(tmp_path, 'rb'))}
	headers = {	"Accept":"application/json",
            	"Connection": "Keep-Alive", 
            	"Cache-Control": "no-cache" ,
            	"Cookie": client_cookie}
	r = requests.post(url , headers = headers , files = files)
	print "SV train:\n", r.text

def test_location_register(locid):
	# POST
	global client_cookie
	params = json.dumps({'locid': locid})
	headers = {"Content-type":"application/json",
				"Accept":"text/plain",
				"Connection": "Keep-Alive", 
				"Cache-Control": "no-cache",
				"Cookie": client_cookie }
	conn = httplib.HTTPConnection("127.0.0.1:8000")
	conn.request("POST","/registerlocation",params,headers)
	r1 = conn.getresponse()
	print 'LOCATION:\n',r1.read()
	conn.close()

def test_location_upload(lat , lon):	
	# POST
	global client_cookie
	params = json.dumps({'latitude':lat , 'longitude':lon})
	headers = {"Content-type":"application/json",
				"Accept":"text/plain",
				"Connection": "Keep-Alive", 
				"Cache-Control": "no-cache" ,
				"Cookie": client_cookie}
	conn = httplib.HTTPConnection("127.0.0.1:8000")
	conn.request("POST","/uploadlocation",params,headers)
	r1 = conn.getresponse()
	print "Upload Loc:"
	print r1.read()
	conn.close()

def test_detect_create():
	global client_cookie
	url = "http://127.0.0.1:8000/detectcreate"
	headers = {	"Accept":"application/json",
            	"Connection": "Keep-Alive", 
            	"Cache-Control": "no-cache" ,
            	"Cookie": client_cookie}
	r = requests.post(url , headers = headers)
	client_cookie = client_cookie + ';' + r.headers['set-cookie']
	print 'Detect Create:\n',client_cookie

def test_detect_result():
	global client_cookie
	url = "http://127.0.0.1:8000/getdetectresult"
	headers = {	"Accept":"application/json",
            	"Connection": "Keep-Alive", 
            	"Cache-Control": "no-cache" ,
            	"Cookie": client_cookie}
	r = requests.post(url , headers = headers)
	print 'Detect Result:\n',r.text

if __name__ == "__main__":
	username = "hagain1"
	password = "1234"
	# User's image
	img_name = "hjr-01.jpg"
	voi_train_name1 = "11.wav"
	voi_train_name2 = "12.wav"
	voi_train_name3 = "13.wav"
	voi_detect_name = "14.wav"

	# Test Method
	# test()
	# test_register(username,password)
	test_login(username,password)
	test_checkstatus()
	# test_location_register(1)
	# test_faceregister(img_name)
	# test_svtrain(voi_train_name1 , voi_train_name2 , voi_train_name3)
	# test_detect_create()
	# 121.475886,31.236797 SH
	# 116.393058, 39.915599	BJ
	# test_location_upload(39.915599 , 116.393058)
	# test_faceverify(img_name)
	# test_svdetect(voi_detect_name)
	# test_detect_result()
