

import urllib
import http.client
import clientlib.lib
import sys

address = "192.168.0.111:9576"
if __name__ == "__main__":
    requrl=""; uname='';passwd=''
    conn = http.client.HTTPConnection(address)
    if clientlib.lib.getres(conn,clientlib.lib.testurl) != b'csuccess':
        print(clientlib.lib.getres(conn,clientlib.lib.testurl))
        print("Failed to connect server,the program will exit")
        exit(1)
    uname,passwd = clientlib.lib.login(conn).split(",")
    print("Input '1'to change your password\nInput '2' to do sth about your missions data\nInput '0' tp exit\n")
    i=input()
    while i:
        if i == '1':
            print("Now input your new password\n")
            newpasswd=input()
            print("Now input your new password again\n")
            newpasswdagain=input()
            if newpasswd == newpasswdagain :
                clientlib.lib.changepasswd(conn,uname,passwd,newpasswd)
                passwd = newpasswd
            else:
                print("It seems different from the first time,R U serious?\n")
        if i == '2':
            print("Input'1' to create a mission,'2' to delete a mission,'3' to alter a mission '4' to consult all your mission")
            print(",'0' to exit\n")
            if clientlib.lib.opreate(conn,uname,passwd) :
                sys.exit(0)
        i=input()
    sys.exit(0)


