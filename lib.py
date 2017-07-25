import sys
import http.client
testurl = "/connectiontest/"



def getres(conn,requrl): #This means get response
    print(requrl)
    conn.request(method="GET", url=requrl)
    response = conn.getresponse()
    return response.read()


def login(conn):
    global uname
    global passwd
    global resp
    print("This is a single client of my server.\n Input'1'to login,'2' to register and '0' to exit\n")
    i = input()
    print(i)
    if i == '1':
        print("Please input your username\n")
        uname = input()
        requrl = "/ifexist/" + uname + "/"
        if getres(conn, requrl) == b'uexist':
            print("Please input your password\n")
            passwd = input()
            print("your pw is" + passwd)
            requrl = "/login/" + uname + "," + passwd + "/"
            resp = getres(conn, requrl)
            if  resp != b"lfailed":
                print("Welcome " + uname + " \n")
                # print("Input '1' to check all your missions,'2' to create a new mission,'0' to exit\n")
            else:
                print("Invalid password ,program will exit now\n")
                exit(1)
        else:
            print("Username doesn't exist, you may register first ,program will exit now\n")
            exit(1)
    elif i == '2':
        print("Please input the username\n")
        uname = input()
        requrl = "/ifexist/" + uname + "/"
        if getres(conn, requrl) != b"uexist":
            passwdflag = 1
            while passwdflag:
                print("Please input your password\n")
                passwd = input()
                print("Please input your password again\n")
                passwdagain = input()
                if passwd != passwdagain:
                    print("The passwords you input are not the same\n")
                else:
                    passwdflag = 0
            requrl = "/register/" + uname + ',' + passwd + '/'
            resp = getres(conn, requrl)
            if  resp != b"rfailed":
                print("Registration succeed.Welcome " + uname + "\n")
        else:
            print("Username exist,please use another one\n")
            login(conn)
    if i == '0':
        sys.exit(0)
    return resp.decode('utf-8')


def changepasswd(conn,cookie,newpasswd):
    url = "/changepasswd/" + cookie + "," + newpasswd+ "/"
    getres(conn,url)


def createmission(conn,cookie,data):
    url = "/mission/" + cookie + ',create,' + data + '/'
    getres(conn,url)


def deletemission(conn, cookie, data):
    url = "/mission/" +cookie + ',delete,' + data + '/'
    getres(conn, url)


def altermission(conn, cookie, data):
    url = "/mission/" + cookie + ',alter,' + data + '/'
    getres(conn, url)


def consultmission(conn, cookie):
    url = "/mission/" + cookie + ',consult,all' + '/'
    print(getres(conn, url))


def opreate(conn,cookie):
    i=input()
    print("Please input data,the format was given in Readme.txt\n")
    data = input()
    if i == '1':
        createmission(conn,cookie,data)
    if i == '2':
        deletemission(conn,cookie,data)
    if i == '3':
        altermission(conn,cookie,data)
    if i == '4':
        consultmission(conn,cookie)
    if i == '0':
        return True
    return False