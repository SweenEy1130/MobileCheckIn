# coding=gbk
from basic import BaseHandler
class JaLoginHandler(BaseHandler):
    def get(self):
        print "JaLogin"
        if not self.get_arguments('jatkt'):
            siteID = 'jasignin20130507'
            uaBaseURL="http://jaccount.sjtu.edu.cn/jaccount/"
            returl = 'http://192.168.1.20:8000/login'
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
            data.decode('utf-8').encode('gbk')
            ProfileData = splitdata(data)
            print data.decode('utf-8').encode('gbk')
            self.set_secure_cookie('uid' , ProfileData['uid'] , None)
            self.set_secure_cookie('sessionid' , ProfileData['ja3rdpartySessionID'] , None)
            if ProfileData['ja3rdpartySessionID'] != iv:
                self.write(self.write({"error":1}))
            self.write({"error":0})

class JaLogoutHandler(BaseHandler):
    def get(self):
        if self.current_user:
            siteID = 'jasignin20130507'
            uaBaseURL="http://jaccount.sjtu.edu.cn/jaccount/"
            returl = 'http://192.168.1.20:8000'
            iv = self.get_secure_cookie('iv')
            redirectURL =  uaBaseURL + "ulogout?sid="+siteID+"&returl="+encrypt(returl,iv)
            self.clear_all_cookies()
            self.redirect(redirectURL)
        else:
            self.redirect(self.write({"error":1}))
