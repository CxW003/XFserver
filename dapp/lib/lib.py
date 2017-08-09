import urllib.parse
import urllib.request
import http.cookiejar
import random
import re


def login(cookie,values,requrl):
    postdata = urllib.parse.urlencode(values).encode()
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'
    opener.addheaders = [("User-agent", user_agent), ("Accept", "*/*"),
                         ('Referer', 'http://202.117.24.14/patroninfo~S3*chx/1177297/items')]
    request = urllib.request.Request(requrl, postdata)
    response = opener.open(request)
    html = response.read()
    return html,cookie


def postvisit(cookie,values,requrl):
    postdata = urllib.parse.urlencode(values).encode()
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'
    opener.addheaders = [("User-agent", user_agent), ("Accept", "*/*"),('Host','www.lib.xjtu.edu.cn'),
                         ('Referer', 'http://202.117.24.14/patroninfo~S3*chx/')]
    request = urllib.request.Request(requrl,postdata)
    response = opener.open(request)
    html = response.read()
    return html


def analyse(html):
    jsonarray = []
    name = re.findall('<span class="patFuncTitleMain">(.*)</span></a></label>', html)
    status = re.findall('<td align="left" class="patFuncStatus">(.*)\n</td>', html)
    callnumber = re.findall('<td align="left" class="patFuncCallNo">(.*)</td>', html)
    i = 0
    while i < len(name):
        bookname,author = name[i].split('/ ')
        alias = ''
        if re.search(':',bookname) !=None:
            partone,parttwo = bookname.split(':')
            parttwo = ':' + parttwo
            if re.search('\s=\s',bookname) != None:
                alias = re.search('\s=\s(.*)',bookname).group(1)
            else:
                alias = '无'
            bookname = re.sub('\s(.*)', '', partone) + parttwo
        else:
            if re.search('\s=\s',bookname) != None:
                alias = re.search('\s=\s(.*)',bookname).group(1)
            else:
                alias = '无'
            bookname = re.sub('\s(.*)', '', bookname)
        deadline = re.search('\d\d-\d\d-\d\d',status[i]).group(0)
        bill = ''
        renewstatus = ''
        expr = re.search('<font color="red">(.*)</font>',status[i])
        if expr != None:
            bill = expr.group(1)
        else:
            bill = '无'
        expr = re.search('<span\s\sclass="patFuncRenewCount">(.*)</span>',status[i])
        if expr != None:
            renewstatus = expr.group(1)
        else:
            renewstatus = '无'
        callnumber[i] = re.sub(' ', '', callnumber[i])
        info = {'name':bookname,
                'alias':alias,
                'author':author,
                'deadline':deadline,
                'bill':bill,
                'renewstatus':renewstatus,
                'callnumber':callnumber[i]}
        jsonarray.append(info)
        i += 1
    return jsonarray


def renew(cookie,values,requrl):
    html,cookie = login(cookie,values,requrl)
    # 全部续借1
    data1={'requestRenewAll':'requestRenewAll'}
    postvisit(cookie,data1,requrl)
    # 全部续借2
    data2 = {'renewall':'是'}
    html = postvisit(cookie,data2,requrl)
    html = html.decode('utf-8')
    return html,cookie

