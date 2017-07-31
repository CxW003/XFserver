from django.shortcuts import render
from dapp.lib import lib
import re
from http import cookiejar
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django import http
import dapp.models
import random
import hashlib
import time
# Create your views here.

global PrimesRepo
global PrimesInitFlag
PrimesInitFlag =0
global KeysUpdateCounter
global PubKeys, PriKeys


def consult(request,offset):
    cons = dapp.models.Accounts.objects.all()
    resp= ''
    # for line in cons:
    #     resp = resp + chr(line.id) + '\t' + line.name + '\t' + line.passwd + '\n'
    if offset == 'all':
        for line in cons:
            resp += chr(line.id) + ',' + line.name + ',' + line.passwd + ';'
        return HttpResponse(resp)
    if offset == 'user':
        for line in cons:
            resp += line.name + ','
        return HttpResponse(resp)
    if offset == 'passwd':
        for line in cons:
                resp +=  line.passwd + ','
        return HttpResponse(resp)
    return HttpResponse('error:no such command')


def register(request,offset):
    name,passwd = offset.split(",")
    if dapp.models.Accounts.objects.filter(name = name).exists()==False:
        regi = dapp.models.Accounts.objects.create(name = name, passwd = passwd)
        random.seed()
        randstr = name + str(random.randrange(0, 9999))
        cookie = hashlib.md5(randstr.encode()).hexdigest()
        # cookie.update(byte(str(time.time()), encoding='utf-8'))
        dapp.models.Sessions.objects.create(userid=regi.id,cookie=cookie)
        return  HttpResponse(cookie)
    else:
        return HttpResponse("rfailed")


def login(request,offset):
    name,passwd = offset.split(",")
    cons = dapp.models.Accounts.objects.filter(name = name)
    if cons.exists()==True:
        cons = dapp.models.Accounts.objects.get(name = name)
        if cons.passwd == passwd:
            flag = True
            while flag:
                random.seed()
                randstr = name + str(random.randrange(0,9999))
                cookie = hashlib.md5(randstr.encode()).hexdigest()
                # cookie.update(byte(str(time.time()), encoding='utf-8'))
                # cookie = cookie.hexdigest()
                ses = dapp.models.Sessions.objects.filter(cookie = cookie)
                if ses.exists()==False:
                    flag = False
                    if dapp.models.Sessions.objects.filter(userid = cons.id).exists():
                        cons = dapp.models.Sessions.objects.get(userid=cons.id)
                        cons.cookie = cookie
                        cons.save()
                    else:
                        dapp.models.Sessions.objects.create(userid=cons.id,cookie=cookie)
                    return HttpResponse(cookie)
    else :
        return HttpResponse("lfailed")


def ifexist(request,offset):
    cons = dapp.models.Accounts.objects.filter(name = offset)
    if cons.exists():
        return HttpResponse ('uexist')
    else:
        return HttpResponse("notexist")


def connectiontest(request):
    return  HttpResponse("csuccess")


def opreate(request,offset):
    cookie,order,data = offset.split(",")
    user = dapp.models.Sessions.objects.filter(cookie = cookie)
    if user != []:
        user = dapp.models.Accounts.objects.get(id = user[0].ownerid)
        if order == "create" :
            type,name,score,period = data.split("_")
            dapp.models.Missions.objects.create(ownerid=user.id, type=type, name=name, score=score, period=period)
            return HttpResponse("csuccess")
        if order == "delete" :
            cons = dapp.models.Missions.objects.filter(id=data)
            if cons[1].ownerid == user.id:
                cons.delete()
                return HttpResponse("dsuccess")
            else:
                return HttpResponse("Mission not found")
        if order == "alter" :
            Mid,type,name,score,period = data.split("_")
            cons = dapp.models.Missions.objects.filter(id=Mid)
            if cons.ownerid == user.id:
                cons.update(type=type, name=name, score=score, period=period)
                return HttpResponse("asuccess")
            else:
                return HttpResponse("Mission not found")
        if order == "consult" :
             if data == "all" :
                cons = dapp.models.Missions.objects.filter(ownerid=user.id)
                res =""
                for line in cons :
                    res += str(line.id) + ',' + line.type + ',' +line.name +','+str(line.score)+','+str(line.period)+','
                res += "`"
                return  HttpResponse(res)
    else:
        return  HttpResponse("Invalid identity")


def changepasswd(request,offset):
    cookie,newpasswd = offset.split(",")
    cons = dapp.models.Sessions.objects.filter(cookie = cookie)
    if cons.exists():
        acc = dapp.models.Sessions.objects.get(cookie = cookie)
        acc = dapp.models.Accounts.objects.get(id = acc.userid)
        acc.update(passwd = newpasswd)
        return  HttpResponse("csuccess")
    else :
        return  HttpResponse("Invalid identity")

@csrf_exempt
def libquery(request):
    global PrimesInitFlag
    if PrimesInitFlag !=1:
        return http.HttpResponseForbidden()
    if request.method != 'POST':
        return http.HttpResponseBadRequest('POST')
    mode = request.POST.get('mode')
    code = request.POST.get('code')
    pin = request.POST.get('pin')
    pin = lib.decrypt(pin,PriKeys)
    print(pin)
    values = {'code':code, 'pin':pin}
    requrl = 'http://202.117.24.14/patroninfo~S3*chx/1177297/items'
    cookie = cookiejar.CookieJar()
    jsonarray = []
    html,cookie = lib.login(cookie,values,requrl)
    html = html.decode('utf-8')
    #已借阅书目分析
    if re.search('未找到借书',html) == None:
        if mode == 'query':
            return HttpResponse('可以查询')
        else:
            jsonarray = lib.analyse(html)
    else:
        return HttpResponse('未找到借书')
    response = HttpResponse(jsonarray)
    response['content-type'] = 'application/json'
    return response


@csrf_exempt
def librenew(request):
    global PrimesInitFlag
    if PrimesInitFlag !=1:
        return http.HttpResponseForbidden()
    if request.method != 'POST':
        return http.HttpResponseBadRequest('POST')
    code = request.POST.get('code')
    pin = request.POST.get('pin')
    pin = lib.decrypt(pin,PriKeys)
    values = {'code':code, 'pin':pin}
    requrl = 'http://202.117.24.14/patroninfo~S3*chx/1177297/items'
    cookie = cookiejar.CookieJar()
    html,cookie = lib.renew(cookie,values,requrl)
    if re.search('<h2>并非所有的续借成功。详见下文。</h2></div>',html) != None:
        cons = re.search('</h2><ul><li>([\s\S]*)</ul><div id="renewfailmsg" style="display:none"\s\sclass="errormessage">',html)
        if cons != None:
            cons = cons.group(1)
            cons = re.sub('<.*?>','',cons)
            return HttpResponse(cons)
        else:
            return HttpResponse('发生了意料之外的错误\n')
    else:
        return HttpResponse('续借成功？')


def getpubkeys(request):
    global PrimesRepo
    global PrimesInitFlag
    global KeysUpdateCounter
    global PubKeys, PriKeys
    if PrimesInitFlag !=1:
        PrimesRepo = []
        file = open('keys.txt', 'r')
        PrimesRepo = file.readlines()[0].split(' ')
        n, e, d = lib.CREATE_KEYS(PrimesRepo)
        KeysUpdateCounter = time.time()
        PubKeys = str(n) + ',' + str(e)
        PriKeys = [n, d]
        file.close()
        PrimesInitFlag =1
    elif time.time() - KeysUpdateCounter >= 7200:
        n, e, d = lib.CREATE_KEYS(PrimesRepo)
        PubKeys = str(n) + ',' + str(e)
        PriKeys = [n, d]
    return HttpResponse(PubKeys)