
testurl = "/connectiontest/"

def getres(conn,requrl): #This means get response
    conn.request(method="GET", url=requrl)
    response = conn.getresponse()
    return response.read()
