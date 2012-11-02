# -*- coding: UTF-8 -*-
import pycurl,urllib,json
import os,sys,time,re,hashlib,random,cStringIO

class Storage:
    def __init__(self):
        self.contents = ''
        self.line = 0

    def store(self, buf):
        self.line = self.line + 1
        self.contents = "%s%s" % (self.contents,buf)

    def __str__(self):
        return self.contents

class T_QQ(object):
    def __init__(self,uin,pwd):
        self.appid="46000101"
        self.uin = uin
        self.pwd = pwd
        self.proxy=""
        self.loginMsg = u"未登录"
        self.curl = pycurl.Curl()
        self.__initCurl()

    def __initCurl(self):
        if(self.curl):
            self.curl.close()
        self.curl=pycurl.Curl()
        self.userAgent= "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1"
        self.curl.setopt(pycurl.USERAGENT,self.userAgent)
        self.curl.setopt(pycurl.COOKIEJAR, "%s_weibo_cookie.txt" % self.uin)
        self.curl.setopt(pycurl.COOKIEFILE, "%s_weibo_cookie.txt" % self.uin)
        self.curl.setopt(pycurl.HTTPHEADER,['Origin: http://t.qq.com',
                                            'Referer: http://api.t.qq.com/proxy.html',
                                            'Accept-Charset: utf-8;q=0.7,*;q=0.3',
                                            'Accept-Language: zh-CN,zh;q=0.8'])
#        self.curl.setopt(pycurl.FOLLOWLOCATION, 1)


    def __initVerifyCode(self):
        '''
                    初始化验证码
        '''
        retrieved_body = Storage()
        retrieved_headers = Storage()
        self.curl.setopt(pycurl.WRITEFUNCTION, retrieved_body.store)
        self.curl.setopt(pycurl.HEADERFUNCTION, retrieved_headers.store)
        checkUrl="http://check.ptlogin2.qq.com/check?uin=%s&appid=%s&r=%s" % (self.uin, self.appid,random.random())

        self.curl.setopt(pycurl.URL,checkUrl)
        self.curl.perform()

        print retrieved_headers
        print retrieved_body
        #得到效验码
        m = re.search(r"'(\d)','(.+)','(.+)'", str(retrieved_body))
        self.verifyCode1 = m.group(2)
        self.verifyCode2 = m.group(3)

        print self.verifyCode1
        print self.verifyCode2

        if m.group(1)=="0":
            print u"免验证码！"
        else:
            print u"需要输入验证码！"
            imgUrl = 'http://captcha.qq.com/getimage?aid=%s&r=%s&uin=%s' % (self.appid,random.random(),self.uin)
            self.curl.setopt(pycurl.URL,imgUrl)
            retrieved_body = Storage()
            retrieved_headers = Storage()
            self.curl.setopt(pycurl.WRITEFUNCTION, retrieved_body.store)
            self.curl.setopt(pycurl.HEADERFUNCTION, retrieved_headers.store)
            with open("code.jpg","wb") as img:
                img.write(retrieved_body)
            self.verifyCode1 = raw_input(u"验证码下载完毕("+os.path.split(os.path.realpath(sys.argv[0]))[0]+os.sep+"code.jpg)，请输入：")
    def __encodePwd(self):
        '''
                    对密码加密
        '''
        def hex_md5hash(myStr):
            return hashlib.md5(myStr).hexdigest().upper()
        def hexchar2bin(uin):
            uin_final = ''
            uin = uin.split('\\x')
            for i in uin[1:]:
                uin_final += chr(int(i, 16))
            return uin_final
        password_1 = hashlib.md5(self.pwd).digest()
        password_2 = hex_md5hash(password_1 + hexchar2bin(self.verifyCode2))
        password_final = hex_md5hash(password_2 + self.verifyCode1.upper())
        self.pwdEncoded = password_final
        print password_final

    def __postLogin(self):
        '''
            提交登录请求
            u:47501900
            p:52C56E92665D47D5BF81A4545E7DFED0
            verifycode:!L0V
            ptlang:2052
            low_login_enable:1
            low_login_hour:720
            css:http://imgcache.qq.com/ptcss/b4/wb/46000101/login1.css
            aid:46000101
            mibao_css:m_weibo
            u1:http://t.qq.com
            ptredirect:1
            h:1
            from_ui:1
            dumy:
            fp:loginerroralert
            action:3-9-3905203
            g:1
            t:1
            dummy:
        '''
        data = {'u':self.uin}
        data['p'] = self.pwdEncoded
        data['verifycode'] = self.verifyCode1
        data['ptlang'] = '2052'
        data['low_login_enable'] = '1'
        data['low_login_hour'] = '720'
        data['css'] = 'http://imgcache.qq.com/ptcss/b4/wb/46000101/login1.css'
        data['aid'] = '46000101'
        data['mibao_css'] = 'm_weibo'
        data['u1'] = 'http://t.qq.com'
        data['ptredirect'] = '1'
        data['h'] = '1'
        data['from_ui'] = '1'
        data['dumy'] = ''
        data['fp'] = 'loginerroralert'
        data['action'] = '3-9-3905203'
        data['g'] = '1'
        data['t'] = '1'
        data['dummy'] = ''

        body = urllib.urlencode(data)
        loginUrl = "http://ptlogin2.qq.com/login?"+body
        self.curl.setopt(pycurl.URL,loginUrl)
        retrieved_body = Storage()
        retrieved_headers = Storage()
        self.curl.setopt(pycurl.WRITEFUNCTION, retrieved_body.store)
        self.curl.setopt(pycurl.HEADERFUNCTION, retrieved_headers.store)
        self.curl.perform()
#        print retrieved_headers
        print retrieved_body
        m = re.search(r"'(\d)','(.+)','(.+)','(.+)','(.+)', '(.+)'", str(retrieved_body))
        if m:
            if m.group(1)!="0": #登录失败
                self.loginMsg = m.group(5)
            else:   #登录成功
                self.loginStatus = True
                self.loginMsg = m.group(5)
        else:   #登录失败，不知道为什么，Fiddler拦截出来的失败结果和上面的格式一样的，程序却不是，只能暂时这样判断
            m = re.search(r"<span style=\"font-size:13px; line-height:17px;\">(.+?)</span></td>",str(retrieved_body),re.DOTALL)
            self.loginMsg = m.group(1).strip()

    def setProxy(self,proxy):
        if(proxy):
            self.curl.setopt(pycurl.PROXY,proxy)

    def login(self):
        self.__initVerifyCode()
        self.__encodePwd()
        self.__postLogin()

    def sendStatus(self,content,picUrl=0):
        uploadPicUrl=''
        if(picUrl):
            uploadPicUrl = self.sendPic(picUrl)
        postUrl = 'http://api.t.qq.com/old/publish.php'
        formdata = {"content":content, "pic":uploadPicUrl, "countType":'', "viewModel":1,"apiType":8,"syncQzone":0,"syncQQSign":0,"attips":''}
        formdata = urllib.urlencode(formdata)
        self.curl.setopt(pycurl.URL,postUrl)
        retrieved_body = Storage()
        retrieved_headers = Storage()
        self.curl.setopt(pycurl.WRITEFUNCTION, retrieved_body.store)
        self.curl.setopt(pycurl.HEADERFUNCTION, retrieved_headers.store)
        self.curl.setopt(pycurl.POSTFIELDS,formdata)
        self.curl.perform()
#        print retrieved_headers
        print retrieved_body
        result = json.loads(retrieved_body.contents.decode("GBK").encode("UTF-8").strip())
        if(result["result"]==0):
            print '%s send status successed. [%s]' % (self.uin,result)
        else:
            print '%s send status failed. [%s]' % (self.uin,result)
    def sendPic(self,imgUrl):

#        self.__initCurl()
        #得到图片的二进制
        c = pycurl.Curl()
        filename='%s.jpg'% random.random()
        c.setopt(pycurl.URL,imgUrl)
        fb = open(filename,'wb')
        c.setopt(pycurl.WRITEFUNCTION, fb.write)
        c.perform()
        fb.flush()
        fb.close()
        c.close()

        #开始上传
        retrieved_body = Storage()
        self.curl.setopt(pycurl.WRITEFUNCTION, retrieved_body.store)
        self.curl.setopt(pycurl.URL,"http://upload.t.qq.com/asyn/uploadpicCommon.php?call=2&uin=%s" % hashlib.md5('123345323'+str(long(time.time()))).hexdigest())
        data=[("Filename",filename),
         ("0","undefined"),
         ("output_type","xml"),
         ("filename",filename),("filename",(pycurl.FORM_FILE,filename,pycurl.FORM_CONTENTTYPE, "application/octet-stream")),
         ("Upload","Submit Query")]
        self.curl.setopt(pycurl.HTTPPOST,data)
        self.curl.perform()

        print retrieved_body.contents.decode("GBK").encode("UTF-8").strip()
        result = json.loads(retrieved_body.contents)
        if(result["result"]==0):
            return result["info"]["url"]
        return ''

    def follow(self,uid,veriCode=''):
        retrieved_body = Storage()
        postUrl = 'http://api.t.qq.com/old/follow.php'
        formdata={"u":uid,"veriCode":veriCode,"lieuId":'',"apiType":8,"apiHost":'http://api.t.qq.com'}
        body = urllib.urlencode(formdata)
        self.curl.setopt(pycurl.URL,postUrl)
        self.curl.setopt(pycurl.WRITEFUNCTION, retrieved_body.store)
        self.curl.setopt(pycurl.POSTFIELDS,body)
        self.curl.perform()
        print retrieved_body.contents.decode("GBK").encode("UTF-8").strip()
#        result = json.loads(retrieved_body.contents,encoding='utf-8')
#        if(result["result"]==0):
        m=re.search(r"result:(.+),msg",retrieved_body.contents)
        if m.group(1) == '0':
            print '%s follow %s sucessed. [%s]' % (self.uin,uid,retrieved_body.contents)
        else:
            print '%s follow %s failed. [%s]' % (self.uin,uid,retrieved_body.contents)

    def uploadHeadPic(self,picUrl):
        #todo
        pass



if __name__ == "__main__":
    tApp = T_QQ("$username","$password")
    #tApp.setProxy("http://localhost:8080")
    tApp.login()
#    tApp.sendPic('http://ecx.images-amazon.com/images/I/41m7YwHS18L._SL160_.jpg')
#    tApp.sendStatus("烦死个人呀！",'http://img.ffffound.com/static-data/assets/6/b531b5dacbd6cd101e1cd1c39f28b1c57df7c913_m.jpg')
#    tApp.follow('aiqingriji9193')
    print tApp.loginMsg
