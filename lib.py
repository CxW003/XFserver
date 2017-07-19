import sys

testurl = "/connectiontest/"



def getres(conn,requrl): #This means get response
    conn.request(method="GET", url=requrl)
    response = conn.getresponse()
    return response.read()


def login(conn):
    uname = ''
    passwd = ''
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
            if getres(conn, requrl) == b"lsuccess":
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
            if (conn, requrl) == b"rsuccess":
                print("Registration succeed.Welcome " + uname + "\n")
        else:
            print("Username exist,please use another one\n")
            login(conn)
    if i == '0':
        sys.exit(0)
    print("your pw is"+passwd)
    return uname+","+passwd


def changepasswd(conn,user,oldpasswd,newpasswd):
    url = "/changepasswd/" + user + "," + oldpasswd + "," + newpasswd+ "/"
    getres(conn,url)


def createmission(conn,username,passwd,data):
    url = "/mission/" + username + ',' + passwd + ',create,' + data + '/'
    getres(conn,url)


def deletemission(conn, username, passwd, data):
    url = "/mission/" + username + ',' + passwd + ',delete,' + data + '/'
    getres(conn, url)


def altermission(conn, username, passwd, data):
    url = "/mission/" + username + ',' + passwd + ',alter,' + data + '/'
    getres(conn, url)


def consultmission(conn, username, passwd):
    url = "/mission/" + username + ',' + passwd + ',consult,all' + '/'
    print(getres(conn, url))


def opreate(conn,username,passwd):
    i=input()
    print("Please input data,the format was given in Readme.txt\n")
    data = input()
    if i == '1':
        createmission(conn,username,passwd,data)
    if i == '2':
        deletemission(conn,username,passwd,data)
    if i == '3':
        altermission(conn,username,passwd,data)
    if i == '4':
        consultmission(conn,username,passwd)
    if i == '0':
        return True
    return False