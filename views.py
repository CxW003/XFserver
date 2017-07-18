from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
import dapp.models


def hello(request):
    html = """<html> <head>  <title>简单的html示例</title> <bgsound src="../music/bendif.mid"> </head>  
    <body background="../img/bg.jpg"> <center> 
     <h3>我的第一个网页</h3> <hr/> 
     <font size=2>  这是我做的第一个网页，欢迎光临！谢谢！ This is my first web. Welcome. </font> </center> </body> </html>"""
    return HttpResponse(html)


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
    regi = dapp.models.Accounts.objects.create(name = name, passwd = passwd)
    return  HttpResponse('rsuccess')

def login(request,offset):
    name,passwd = offset.split(",")
    cons = dapp.models.Accounts.objects.get(name = name)
    if cons.id > 1 and cons.passwd == passwd:
        return HttpResponse("lsuccess")
    else :
        return HttpResponse("lfailed")

def ifexist(request,offset):
    cons = dapp.models.Accounts.objects.get(name = offset)
    if cons.id > 0:
        return HttpResponse ("uexist")
    else:
        return HttpResponse("unexist")

def connectiontest(request):
    return  HttpResponse("csuccess")

def opreate(request,offset):
    name,passwd,order,data = offset.split(",")
    user = dapp.models.Accounts.objects.get(name = name)
    if user.id > 0 and user.passwd == passwd:
        if order == "create" :
            type,name,score,period = data.split("_")
            dapp.models.Missions.objects.create(ownerid=user.id, type=type, name=name, score=score, period=period)
            return HttpResponse("csuccess")
        if order == "delete" :
            dapp.models.Missions.objects.filter(id=data).delete()
            return HttpResponse("dsuccess")
        if order == "alter" :
            Mid,type,name,score,period = data.split("_")
            dapp.models.Missions.objects.filter(id=Mid).update(type=type, name=name, score=score, period=period)
            return HttpResponse("asuccess")
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

