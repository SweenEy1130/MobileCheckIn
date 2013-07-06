# coding=gbk
# $File: jalogin.py
# $Date: Sat Jun 22 13:45:27 2013 +0800
# $Author: ronnie.alonso@gmail.com
#
#      0. You just DO WHAT THE FUCK YOU WANT TO.
from basic import BaseHandler
from datetime import *
from setting import port,domain,siteID
from jaccount import encrypt , decrypt , find , splitdata
import random,string,json
import faceppKit


"""用户JACCOUNT LOGIN
API:    http://localhost:port/jalogin
RESPONSE:{  "error":0}
0:success
1:hacking attempt
3:face++ person_create error
"""
class JaLoginHandler(BaseHandler):
    def get(self):
        if not self.get_arguments('jatkt'):
            uaBaseURL="http://jaccount.sjtu.edu.cn/jaccount/"
            returl = 'http://'+domain+':'+str(port)+'/jalogin'
            iv = string.join(random.sample('1234567890abcdef',8),'')
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
            data.decode('utf-8').encode('gbk')
            ProfileData = splitdata(data.decode('utf-8'))
            # print data.decode('utf-8')
            if ProfileData['ja3rdpartySessionID'] != iv:
                self.write({"error":1})
                return
            self.update_user(ProfileData)
            self.set_secure_cookie('uid' , ProfileData['id'] , None)
            self.set_cookie('chiname' , ProfileData['chinesename'] , None)
            self.write({"error":0})

    def update_user(self , profile):
        uid = profile['id']
        info = self.db.query('SELECT UID,LOCID,DEPARTMENT,CHINAME FROM USER WHERE UID = %s;' % (uid))
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        chiname = profile['chinesename']
        username = profile['uid']
        dept = profile['dept']
        if not info:
            sql = "INSERT INTO USER(UID,USERNAME,CHINAME,DEPARTMENT,LOCID,CREATETIME)\
                VALUES(%s,\'%s\',\'%s\',\'%s\',1,\'%s\')" % (uid,username,chiname,dept,now)
            res = self.db.execute(sql)
            
            # FACE++
            try:
                url = facepp_kit.CreatePerson(uid,u'Students')
                response = urllib2.urlopen(url)
                person_create = response.read()
            except urllib2.URLError, e:
                if not hasattr(e, "code"):
                    raise
                self.write({'error':3 , 'info':json.loads(e.read())['error']})
        else:
            info=info[0]
            if (not info['LOCID']) or (not info['DEPARTMENT']) or(not info['CHINAME']):
                sql="UPDATE USER SET USERNAME=\'%s\',LOCID=1,DEPARTMENT=\'%s\',CHINAME=\'%s\' WHERE UID=%s;" %\
                    (username,dept,chiname,uid)
                res=self.db.execute(sql)

"""用户JACCOUNT LOGOUT
API:    http://localhost:port/jalogout
RESPONSE:{  "error":0}
"""            
class JaLogoutHandler(BaseHandler):
    def get(self):
        if self.current_user:
            uaBaseURL="http://jaccount.sjtu.edu.cn/jaccount/"
            returl = 'http://'+domain+':'+str(port)
            iv = self.get_secure_cookie('iv')
            redirectURL =  uaBaseURL + "ulogout?sid="+siteID+"&returl="+encrypt(returl,iv)
            self.clear_all_cookies()
            self.redirect(redirectURL)
            return
        else:
            self.write({"error":1})
            return
