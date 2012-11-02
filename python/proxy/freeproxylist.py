# -*- coding: UTF-8 -*-
__author__ = 'simon'

import urllib,pycurl,cStringIO
import sys,re,gzip
from BeautifulSoup import BeautifulSoup

def getProxyList():
    curl = pycurl.Curl()
    curl.setopt(pycurl.COOKIEFILE,'freeproxylists.cookie')
    curl.setopt(pycurl.COOKIEJAR,'freeproxylists.cookie')
    curl.setopt(pycurl.FOLLOWLOCATION,1)
    userAgent= "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.11 (KHTML, like Gecko) Ubuntu/12.04 Chromium/20.0.1132.47 Chrome/20.0.1132.47 Safari/536.11"
    curl.setopt(pycurl.USERAGENT,userAgent)
    headers = ["Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
               "Accept-Encoding: gzip,deflate,sdch",
               "Accept-Language: en,zh-CN;q=0.8,zh;q=0.6",
               "Accept-Charset: GBK,utf-8;q=0.7,*;q=0.3"]
    curl.setopt(pycurl.HTTPHEADER,headers)

    curl.setopt(pycurl.VERBOSE,1)

    curl.setopt(pycurl.PROXY,'http://192.168.60.15:808')


    urls=["http://freeproxylists.net/"]

    for i in range(2,3):
        urls.append("http://freeproxylists.net/?page=%d" % i)

    for url in urls:
        f = cStringIO.StringIO()
        curl.setopt(pycurl.URL,url)
        curl.setopt(pycurl.WRITEFUNCTION,f.write)
        curl.perform()

        html = gzip.GzipFile(fileobj=cStringIO.StringIO(f.getvalue())).read()
        soup = BeautifulSoup(html)
#        print soup
        odds = soup.findAll("tr","Odd")
        for odd in odds:
            print odd.td[0]

if __name__ == "__main__":
    getProxyList()
