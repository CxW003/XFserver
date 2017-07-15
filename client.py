

import urllib
import http.client
import clientlib.lib

if __name__ == "__main__":
    uname = "";passwd="";requrl=""
    conn = http.client.HTTPConnection("192.168.0.111:9576")
    if clientlib.lib.getres(conn,clientlib.lib.testurl) != "csuccess":
        print("Failed to connect server,the program will exit")
        exit(1)
    print("This is a single test of my server.\n Input'1'to login,'2' to register and '0' to exit\n")
    i = input()
    if i == 1:
        print ("Please input your username\n")
        uname = input()
        requrl = "/ifexist/" + uname + "/"
        if clientlib.lib.getres(conn,requrl) == "uexist" :
            print("Please input your password\n")
            passwd = input()
            requrl = "/login/" + uname + "," + passwd + "/"
            if clientlib.lib.getres(conn,requrl) == "lsuccess":
                print ("Welcome "+uname+" \n")
                print ("Input '1' to check all your missions,'2' to create a new mission,'0' to exit\n")
            else :
                print("Invalid password ,program will exit now\n")
                exit(1)
        else:
            print("Username doesn't exist, you may register first ,program will exit now\n")
            exit(1)
    elif i == 2 :
        print ("Please input the username\n")
        uname = input()
        requrl = "/ifexist/" + uname + "/"
        if clientlib.lib.getres(conn,requrl) != "uexist" :
            passwdflag = 1
            while passwdflag :
                print("Please input your password\n")
                passwd = input()
                print("Please input your password again\n")
                passwdagain = input()
                if passwd != passwdagain :
                    print("The passwords you input are not the same\n")
                else:
                    passwdflag = 0
            requrl = "/register/" + uname + ','+ passwd + '/'
            if clientlib.lib.getres(conn,requrl) == "rsuccess":
                print("Registration succeed.Welcome " + uname +"\n")
        else:
            print ("Username exist,please use another one\n")


