# -*- coding: UTF-8 -*-
__author__ = 'simon'

import pycurl,urllib
import os,time,re,random
import json,cStringIO
from utils.namegen import getBoyName

class Storage:
    def __init__(self):
        self.contents = ''
        self.line = 0

    def store(self, buf):
        self.line = self.line + 1
        self.contents = "%s%s" % (self.contents,buf)

    def __str__(self):
        return self.contents

class SohuWeiboAutoRegister:

    def __init__(self):
        self.curl = pycurl.Curl()
        self.logfile = open('accounts.txt','a')
        self.__initCurl()
        self.__init_cookie()
        self.__loadProxy('proxies.txt')

    def __initCurl(self):
        if(self.curl):
            self.curl.close()
        self.curl=pycurl.Curl()
        self.userAgent= "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1"
        self.curl.setopt(pycurl.USERAGENT,self.userAgent)
        self.curl.setopt(pycurl.CONNECTTIMEOUT,10)
        self.curl.setopt(pycurl.TIMEOUT,10)
        self.curl.setopt(pycurl.COOKIEJAR, "sohu_reg_cookie.txt")
        self.curl.setopt(pycurl.COOKIEFILE, "sohu_reg_cookie.txt")
        self.curl.setopt(pycurl.HTTPHEADER,['Referer: http://t.sohu.com/jingxuan',
                                            'Origin: http://t.sohu.com',
                                            'Accept-Charset: GBK,utf-8;q=0.7,*;q=0.3',
                                            'Accept-Language: zh-CN,zh;q=0.8',
                                            'Content-Type: application/x-www-form-urlencoded',
                                            'Accept: application/json, text/javascript, */*; q=0.01'])

    def __loadProxy(self,filename):
        self.proxies=[]
        f = open(filename,'r')
        while 1:
            proxy = f.readline()
            if proxy:
                self.proxies.append(proxy.strip())
            else:
                break
        f.close()


    def regist(self,nickname):
#        self.__initCurl()
        reTwitterUrl = "http://t.sohu.com/guide/discover/reTwitter"
        self.curl.setopt(pycurl.URL,reTwitterUrl)
        msgid = random.choice(self.ids)
        formdata = {"msgid":msgid,"type":"1284122","at":msgid,"msg":"&#43;2","#43;2":"","content":"","userName":nickname}
        formdata = self.__urlencode_utf8(formdata);
#        print formdata
        self.curl.setopt(pycurl.POSTFIELDS,formdata)
        retrieved_body = Storage()
        retrieved_headers = Storage()
        self.curl.setopt(pycurl.WRITEFUNCTION, retrieved_body.store)
        self.curl.setopt(pycurl.HEADERFUNCTION, retrieved_headers.store)

        self.curl.perform()

#        print retrieved_headers
#        print retrieved_body
        resultContents = retrieved_body.contents.decode("GBK").encode("UTF-8")
        result = json.loads(resultContents,'UTF-8')
#        print resultContents
#        result
        if result['status'] == 0 and result.has_key("data"):
            print resultContents.strip()
#            self.logfile.write("%s %s %s" % (result["data"]["passport"],result["data"]["password"],result["data"]["userName"]))
            self.logfile.write(resultContents.strip()+"\r\n")
            self.logfile.flush()
        else:
            print u"注册失败"




    def __init_cookie(self):
        url = 'http://t.sohu.com/jingxuan'
        f = cStringIO.StringIO()
        self.curl.setopt(pycurl.URL,url)
        self.curl.setopt(pycurl.WRITEFUNCTION, f.write)
#        self.curl.setopt(pycurl.VERBOSE,1)
        self.curl.setopt(pycurl.FOLLOWLOCATION,1)
        self.curl.perform()
        self.ids = re.findall(r'"http://t.sohu.com/m/(\d+)"',f.getvalue())
#        print f.getvalue()
        print self.ids
        f.close()





    def __urlencode_utf8(self,params):
        from urllib import quote_plus
        if hasattr(params, 'items'):
            params = params.items()
        return '&'.join(
            (quote_plus(k, safe='/') + '=' + v
                for k, v in params))

    def checkNickname(self,nickname):

#        self._init_cookie()
        checkNicknameUrl = "http://t.sohu.com/regist/checkNickName"
        self.curl.setopt(pycurl.URL,checkNicknameUrl)
        nickname = unicode(nickname,'utf-8')
        nickname = nickname.encode('unicode_escape').upper().replace("\\U","%u")
#        formdata = "nickname:%s" % nickname
        formdata = {'nickname':nickname}
        formdata = self.__urlencode_utf8(formdata)
#        print formdata
        self.curl.setopt(pycurl.POSTFIELDS,formdata)
        retrieved_body = Storage()
        retrieved_headers = Storage()
        self.curl.setopt(pycurl.WRITEFUNCTION, retrieved_body.store)
        self.curl.setopt(pycurl.HEADERFUNCTION, retrieved_headers.store)
        self.curl.perform()
#        print retrieved_headers
        print retrieved_body.contents.decode("GBK").encode("UTF-8").strip()
        result = json.loads(retrieved_body.contents,encoding="GBK")
        if result['status'] == 0:
            return True,nickname
        else:
            return False,''

    def setProxy(self,proxy):
        if(proxy):
            self.curl.setopt(pycurl.PROXY,proxy)

    def setRandomProxy(self):
        proxy = 'http://'+random.choice(self.proxies)
        print 'Proxy: %s' % proxy
        self.curl.setopt(pycurl.PROXY,proxy)




if __name__ == "__main__":
    autoReg = SohuWeiboAutoRegister()
#    autoReg.setProxy("http://187-032-127-163.static.ctbctelecom.com.br:3128")
    while 1:
        try:
            try:
                os.remove('sohu_reg_cookie.txt')
            except:
                pass
            name = getBoyName()
        #        print name
            autoReg.setRandomProxy();

            result,nickname = autoReg.checkNickname(getBoyName())
            if result:
                autoReg.regist(nickname);
            else:
                continue
        except:
            pass

        time.sleep(1)
    autoReg.logfile.close()




