from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
import dapp
def hello(request):
    html = """<html> <head>  <title>简单的html示例</title> <bgsound src="../music/bendif.mid"> </head>  
    <body background="../img/bg.jpg"> <center> 
     <h3>我的第一个网页</h3> <hr/> 
     <font size=2>  这是我做的第一个网页，欢迎光临！谢谢！ This is my first web. Welcome. </font> </center> </body> </html>"""
    return HttpResponse(html)

def baidu(request):
    return render(request,"baidu.html")
    #return render_to_response("baidu.html")

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

def connectiontest(request):
    return  HttpResponse("csuccess")