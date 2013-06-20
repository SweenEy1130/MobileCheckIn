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

def test():
	# GET
	conn = httplib.HTTPConnection("127.0.0.1:8000")
	conn.request("GET","/test")
	r1 = conn.getresponse()
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
	conn.request("POST","/jalogin",params,headers)
	r1 = conn.getresponse()
	print "User login:"
	print r1.read()
	conn.close()

if __name__ == "__main__":
	test()
	username = "ronnie_alonso"
	password = "LZheng1130"
	test_login(username,password)

