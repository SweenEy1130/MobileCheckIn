import urllib2,urllib
import json,string
import sys,json
# https://jaccount.sjtu.edu.cn/jaccount/ulogin?sid=jasignin20130507&returl=CCnDQOR9CCcvMfuCDFVlnmGOJTkYl8F9pbMfritbC6Rlimm7jR/DTpE=&se=CDMBLNJZ1PfvYyE8SNeXnudXxaturktGZQ==
def test_jalogin():
	url = "https://jaccount.sjtu.edu.cn/jaccount/login"
	values = {
				'name':'ronnie_alonso' , 
				'pass':'LZheng1130' , 
				'sid': 'jasignin20130507' ,
				'returl':"CCnDQOR9CCcvMfuCDFVlnmGOJTkYl8F9pbMfritbC6Rlimm7jR/DTpE=",
				'se':"CDMBLNJZ1PfvYyE8SNeXnudXxaturktGZQ=="
				}
	headers = {
			"Content-Type":"application/x-www-form-urlencoded",     
            "Referer":"http://127.0.0.1:8000/"
           };
	data = urllib.urlencode(values)
	req = urllib2.Request(url, data,headers)
	response = urllib2.urlopen(req)
	print response.info() , response.read() , response.geturl()

if __name__ == "__main__":
	test_jalogin()