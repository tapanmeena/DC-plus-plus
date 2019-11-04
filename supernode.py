# broadcasting port number : 44444
# livestatus port number : 12121
# handleFile() sharing port : 9005
# supernode to supernode communication PORT : 9999
# showFile : 9001
# findFile : 9002, 9003
# reqHandler : 9090
# add superNode broadcast req : 11000
# superNode file update info : 11001
# ACK to supernode for assigning SuperNode 8090
# superNode to supernode file info sharing(first time only) : 11002

import socket
import subprocess
import threading
import os
import time
import pickle
from collections import defaultdict

#PORT Mappings 
PORT_updateSuperNode = 11001
PORT_superNodeFileCache = 11002
PORT_sync = 9191

myIPAddr = ""
# containing objects of Node
childNodes = {} #{IPAddr->Node}
fileCache = defaultdict(list) #{fileName -> [IPAddr,...]}
superNodeList = []

def myIP():
    global myIPAddr
    bashCommand = 'hostname -I | awk \'{print $1}\''
    IPAddr = subprocess.check_output(['bash','-c', bashCommand])
    myIPAddr = IPAddr.strip('\n')

# ---------------------Inter Super node communication---------------------

def recvFileCache():
    print ("----inside recv file cache---")
    global fileCache
    tempCache = recvObj(PORT_superNodeFileCache, 10)
    if len(fileCache)==0 and tempCache is not None:
        print tempCache
        fileCache = tempCache

def sendFileCache(ipAddr):
    sendObj(PORT_superNodeFileCache, ipAddr, fileCache)

# run on a thread to alter the supernode list
def setSuperNodes():
    getSuperNodes1()
    # accept requests to become superNode
    sNode = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    sNode.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sNode.bind(("", 11000))
    while True:
        # continuously listen for broadcast msgs
        data, addr = sNode.recvfrom(5096)
        if data != '':
            if addr[0] not in superNodeList and addr[0]!= myIPAddr:
                print "New Connected SuperNode :-"+addr[0]+"-"
                getSuperNodes2(addr[0])
                superNodeList.append(addr[0])

# send a broadcast message once to add your ip to all other supernodes.
def getSuperNodes1():
    broadcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    broadcast.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Set a timeout so the socket does not block
    # indefinitely when trying to receive data.
    broadcast.settimeout(5)
    broadcast.bind(("", 44444))

    message = "I'm a superNode"

    broadcast.sendto(message, ('<broadcast>', 11000))
    broadcast.close()
    sNode = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    sNode.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sNode.bind(("", 11000))
    sNode.settimeout(2)
    tempaddr = ""
    try:
        data, addr = sNode.recvfrom(5096)
        tempaddr = addr[0]
        if data != '':
            if addr[0] not in superNodeList and addr[0]!= myIPAddr:
                print "New Connected SuperNode2 :-"+addr[0]+"-"
                superNodeList.append(addr[0])
    except socket.error, exc:
        print "Some Error in Supernode 1",exc
    sNode.close()

    #sync messages

    TCP_IP = tempaddr
    TCP_PORT = PORT_sync
    BUFFER_SIZE = 5096
    p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        p.connect((str(TCP_IP), TCP_PORT))
        p.send("hola, amoebas!")
        p.close()
    except socket.error , exc:
        print "Error Caught : ",exc

    recvFileCache()
    
    print("________________cache after rec cache________________")
    print(fileCache)
    print("______________________________________________________")

def getSuperNodes2(addr):
    broadcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    broadcast.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Set a timeout so the socket does not block
    # indefinitely when trying to receive data.
    broadcast.settimeout(5)
    broadcast.bind(("", 44444))

    message = "I'm a superNode"

    broadcast.sendto(message, ('<broadcast>', 11000))
    broadcast.close()
    # time.sleep(4)
    #sync messages
    
        
    TCP_IP = myIPAddr
    TCP_PORT = PORT_sync
    BUFFER_SIZE  = 5096
    tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    tcpsock.bind((TCP_IP, TCP_PORT))
    # tcpsock.settimeout(tout) 
    try:
        tcpsock.listen(5)
        (conn, (ip, port)) = tcpsock.accept()
        msg = conn.recv(5096)
        tcpsock.close()
    except socket.error as e:
        print "files addition socket timeout : " + TCP_IP
        tcpsock.close()
        return
    tcpsock.close()


    sendFileCache(addr)
    print("------------------cache after send file------------")
    print(fileCache)
    print("________________________________________________")

# continuously listen for updates regarding the files meta information
# maintain same set of file information across all superNodes.
def getUpdates():
    BUFFER_SIZE = 5096
    tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("---------in get Update s->>>>>>>>"+str(myIPAddr)+"<<<<<<<,,")

    tcpsock.bind((myIPAddr, PORT_updateSuperNode))

    while True:
        tcpsock.listen(5)
        print "----update superNode waiting=--------"
        (conn, (ip,port)) = tcpsock.accept()
        print 'Got connection from ', (ip,port)
        data, addr = conn.recvfrom(5096)
        if data !='':
            print "---------------------updating superNode -------------------"
            print data
            
            msg = pickle.loads(data)
            
            for x in msg:
                print x
                if(x[5] == "add"):
                    print "adding files -->"+ myIPAddr +"-->fileName-->"+ x[0]
                    childNodes[myIPAddr].fileMap[x[0]] = File(x[0], x[1], x[2], x[3], x[4])
                    fileCache[x[0]].append(myIPAddr)
                elif(x[5] == "delete"):
                    print "deleting files -->"+ myIPAddr+"-->filename-->"+ x[0]
                    del(childNodes[myIPAddr].fileMap[x[0]])
                    fileCache[x[0]].remove(myIPAddr)
                    if(len(fileCache[x[0]])==0):
                        del(fileCache[x[0]])
        conn.close()
    tcpsock.close()

# Whenever our fileCache is updated send the updated file meta information to
# other supernodes.
def sendUpdates(data):
    print("___--inside send updates _______")
    for x in superNodeList:
        print("_____superNode fella->"+str(x)+"<_____")
        sendObj(PORT_updateSuperNode, x, data)

# -------------------------end super node comm----------------------------
class Node:
    def __init__(self, IPAddr, liveStatus) :
        self.IPAddr = IPAddr
        self.liveStatus = liveStatus
        self.fileMap = {}
        self.count = 0
    def __eq__(self, other):
        if not isinstance(other, Node):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.IPAddr == other.IPAddr

class File: 
    def __init__(self, name, h1, h2, h3, h4):
        self.name = name
        self.h1 = h1
        self.h2 = h2
        self.h3 = h3
        self.h4 = h4

# recv an object via TCP socket
def recvObj(port, tout = 4):
    TCP_IP = myIPAddr
    TCP_PORT = port
    BUFFER_SIZE  = 5096
    tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    tcpsock.bind((TCP_IP, TCP_PORT))
    tcpsock.settimeout(tout) 
    try:
        tcpsock.listen(5)
        (conn, (ip, port)) = tcpsock.accept()
        msg = conn.recv(5096)
        data = pickle.loads(msg)
        tcpsock.close()
        return data 
    except socket.timeout as e:
        print "files addition socket timeout : " + TCP_IP
        tcpsock.close()
        return
    tcpsock.close()

# send an object from TCP sockets
def sendObj(port, IPAddr, obj):
    TCP_IP = str(IPAddr)
    TCP_PORT = port
    BUFFER_SIZE = 5096

    #convert object to serial stream  
    msg = pickle.dumps(obj)
    
    p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        p.connect((str(TCP_IP), TCP_PORT))
        p.send(msg)
        p.close()
    except socket.error , exc:
        print "Error Caught : ",exc

# thread running continuously to cater to the requests made by the clients
# port 9090
def reqHandler():
    sNode = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    sNode.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sNode.bind(("", 9090))
    while True:
        # continuously listen for broadcast msgs
        data, addr = sNode.recvfrom(5096)
        if data == "showFiles" :
            print "Inside reqhandler showfile :",addr[0]
            showFile(addr[0])
        elif data == "findFile":
            print "Inside reqhandler Findfile :",addr[0]
            findFile(addr[0])
        elif data == "downloadComplete"
            print "Download Complete"
            transfer_done(addr[0])

# returns the list of all filenames from alive nodes.
# PORT 9001
def showFile(IPAddr):
    result =[]
    for x in fileCache:
        result.append(x)
    sendObj(9001, IPAddr, result)
    
# gets filename and returns list of IP
# PORT 9002, 9003
def findFile(IPAddr):
    filename = recvObj(9002)
    print "Filename  : ",filename
    sendObj(9003, IPAddr, loadBal(filename))

# load balancer, finds the IP addr with the min no of live requests
def loadBal(filename):
    minimum = -1
    resIP = ""
    for x in fileCache[filename]:
        if(childNodes[x].count<minimum):
            resIP = x.IPAddr
            minimum = x.count
    childNodes[resIP].count+=1
    return resIP

def transfer_done(IPAddr):
    if(childNodes[IPAddr].count>0):
        childNodes[IPAddr].count-=1

def handleFiles(IPAddr):
    print ("_______handle files _________"+ str(IPAddr)+"_______________")
    
    TCP_IP = myIPAddr
    
    TCP_PORT = 44445
    BUFFER_SIZE  = 5096
    tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    tcpsock.bind((TCP_IP, TCP_PORT))
    tcpsock.settimeout(10) 
    try:
        tcpsock.listen(5)
        (conn, (ip, port)) = tcpsock.accept()
        msg = conn.recv(5096)
        # print ("____________________")
        print msg
        # print ("____________________")

        data = pickle.loads(msg)
        #push file updates to all the supernodes
        sendUpdates(data)
        print "----------"
        for x in data:
            print x
            if(x[5] == "add"):
                print "adding files -->"+ IPAddr +"-->fileName-->"+ x[0]
                childNodes[IPAddr].fileMap[x[0]] = File(x[0], x[1], x[2], x[3], x[4])
                print("_____________debugging ki ma_________________________")
                print("filecahce->", fileCache)
                print("x[0]", x[0])
                print("IPADDR->", IPAddr)
                print(fileCache[x[0]])
                print("_______________________________________________________")
                fileCache[x[0]].append(IPAddr)
            elif(x[5] == "delete"):
                print "deleting files -->"+ IPAddr+"-->filename-->"+ x[0]
                del(childNodes[IPAddr].fileMap[x[0]])
                fileCache[x[0]].remove(IPAddr)
                if(len(fileCache[x[0]])==0):
                    del(fileCache[x[0]])

        print "----------"

        x = childNodes[IPAddr]
        for y in x.fileMap:
            print(x.fileMap[y].name)                     
        tcpsock.close()
        print "Exiting Try Staement in Handle Files"
        return
    except socket.error ,exc:
        print "Error in HandleFile : ",exc
        print "files addition socket timeout : " + TCP_IP
        tcpsock.close()
        return
    print "Exiting Handle Files"

def assignSuperNode():
    # accept requests to become superNode
    sNode = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    sNode.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sNode.bind(("", 37020))
    while True:
        # continuously listen for broadcast msgs
        data, addr = sNode.recvfrom(5096)
        if data != '':
            # print("____________"+data+"___________")
            # print("____________"+myIPAddr+"___________")
            # print("____________"+addr[0]+"___________")

            sNode.sendto(myIPAddr, addr)
            print "Receive New Connection : ",addr[0]
            ## ACK Listening Start
            tempNode = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
            tempNode.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            tempNode.bind((myIPAddr, 8090))
            tempNode.settimeout(5)
            try:
                data1, addr1 = tempNode.recvfrom(5096)
                tempNode.close()
                print "Data :",data1," Message :",addr[0]
                if data1 == "ACK":
                    if childNodes.get(addr[0]) is not None:
                        childNodes[addr[0]].liveStatus = True
                        print('----------dead to alive-------')
                        
                        #TODO
                        handleFiles(addr[0])

                    else:
                        childNodes[addr[0]]=(Node(addr[0], True))
                        print('------adding new node ----------')
                        
                        #TODO 
                        handleFiles(addr[0])
            except socket.timeout as e:
                print "Error caught during super Node Assignment :",e
            ## ACK Listening END
            
def heartBeat():
    print 'Inside HeartBeat'
    isCheck = False
    time.sleep(10)
    while True:
        # TCP_IP = "10.196.700.181"
        for x in list(childNodes):
            child = childNodes[x]
            if(child.liveStatus):
                print "Child IP : "+child.IPAddr
                TCP_IP = child.IPAddr
                TCP_PORT = 12121
                BUFFER_SIZE  = 5096

                #convert object to serial stream  
                msg = "You there???"
                msg = pickle.dumps(msg)
                
                p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    p.connect((TCP_IP, TCP_PORT))
                    p.send(msg)
                    p.close()
                    print "Node is Alive :) " + TCP_IP
                except socket.error , exc:
                    print "Error Caught in live status : ",exc
                    child.liveStatus = False
                    print "Node is Dead:( ",TCP_IP
        time.sleep(200)

# def SupernodeToSupernode():
#     supernodeIPList = ['10.196.7.181']
    
if __name__ ==  "__main__": 
    
    myIP()

    threads = []
    # print ID of current process 
    # print("ID of process running main program: {}".format(os.getpid())) 
  
    # print name of main thread 
    # print("Main thread name: {}".format(threading.main_thread().name)) 

    setSuper = threading.Thread(target=setSuperNodes, name='setSuper')
    # Run forever to Assign Super node to Client
    t1 = threading.Thread(target=assignSuperNode, name='t1')
    # Run forever to check File Server Live Status (Alive/Dead)
    hbt = threading.Thread(target = heartBeat, name = 'heartBeat')
    reqH = threading.Thread(target = reqHandler, name = 'reqH')
    getU = threading.Thread(target = getUpdates, name = 'getU')


    threads.append(setSuper)
    threads.append(t1)
    threads.append(hbt)
    threads.append(reqH)
    threads.append(getU)
    # starting threads 

    setSuper.start()
    getU.start()
    t1.start()
    hbt.start()
    # sts.start()
    reqH.start()

    # wait until all threads finish 
    getU.join()
    setSuper.join()
    t1.join()
    hbt.join()
    reqH.join()

