# coding=gbk
from pyDes import *
import string,random,base64,urllib2,re,sys
from tornado.web import HTTPError

def find(s,regex):
    import re
    match = re.search(regex, s)
    if match:
        result = match.group()
    else:
        result = ""
    return result

def splitdata(data):
    a = data.split()
    c = {'type':'ProfileData'}
    try:
        for i in range(0,10):
            a[i] = a[i].split('=')
    except IndexError:
        pass
    for b in a:
        c[b[0]] = b[1]
    return c
    
def keydata():
    f_path = sys.path[0]+"/jasignin20130507_desede.key"
    f = open(f_path,'rb')
    f_data = f.read()
    f.close()
    return f_data    

def encrypt(data,iv):
    key = keydata()
    k = triple_des(key,CBC,iv,pad=None,padmode=PAD_PKCS5)
    d = k.encrypt(data)
    data = chr(8)+iv+d
    data = urllib2.quote(base64.b64encode(data))
    return data

def decrypt(data,iv):
    key = keydata()
    try:
        data = base64.b64decode(urllib2.unquote(data))
        data = data[1:]
        d = triple_des(key,CBC,iv,pad=None,padmode=PAD_PKCS5)
        k = d.decrypt(data)
    except TypeError,ValueError:
        raise HTTPError(404)
    return k
