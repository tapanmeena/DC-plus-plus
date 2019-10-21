# broadcasting port number : 44444
# livestatus port number : 12121
# handleFile() sharing port : 9005
# supernode to supernode communication PORT : 9999
# showFile : 9001
# findFile : 9002, 9003
# reqHandler : 9090
# add superNode broadcast req : 11000
# superNode file update info : 11001

import socket
import subprocess
import threading
import os
import time
import pickle
from collections import defaultdict

myIPAddr = ""

def myIP():
    global myIPAddr
    bashCommand = 'hostname -I | awk \'{print $1}\''
    IPAddr = subprocess.check_output(['bash','-c', bashCommand])
    myIPAddr = IPAddr.strip('\n')

# ---------------------Inter Super node communication---------------------

# run on a thread to alter the supernode list
def setSuperNodes():
    # accept requests to become superNode
    sNode = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    sNode.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sNode.bind(("", 11000))
    while True:
        # continuously listen for broadcast msgs
        data, addr = sNode.recvfrom(1024)
        if data != '':
            print "New Connected SuperNode :-"+addr[0]+"-"
            if addr[0] not in superNodeList:
                superNodeList.append(addr[0])

# send a broadcast message once to add your ip to all other supernodes.
def getSuperNodes():
    broadcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    broadcast.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Set a timeout so the socket does not block
    # indefinitely when trying to receive data.
    broadcast.settimeout(5)
    broadcast.bind(("", 44444))

    message = "I'm a superNode"

    broadcast.sendto(message, ('<broadcast>', 11000))
    broadcast.close()

#continuously listen for updates regarding the
# def getUpdates():
    
# def sendUpdates():

# -------------------------end super node comm----------------------------
class Node:
    def __init__(self, IPAddr, liveStatus) :
        self.IPAddr = IPAddr
        self.liveStatus = liveStatus
        self.fileMap = {}
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

# containing objects of Node
childNodes = {} #{IPAddr->Node}
fileCache = defaultdict(list) #{fileName -> [IPAddr,...]}

# recv an object via TCP socket
def recvObj(port):
    TCP_IP = myIPAddr
    TCP_PORT = port
    BUFFER_SIZE  = 1024
    tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    tcpsock.bind((TCP_IP, TCP_PORT))
    tcpsock.settimeout(10) 
    try:
        tcpsock.listen(5)
        (conn, (ip, port)) = tcpsock.accept()
        msg = conn.recv(1024)
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
    BUFFER_SIZE = 1024

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
        data, addr = sNode.recvfrom(1024)
        if data == "showFiles" :
            print "Inside reqhandler showfile :",addr[0]
            showFile(addr[0])
        elif data == "findFile":
            print "Inside reqhandler Findfile :",addr[0]
            findFile(addr[0])

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
    sendObj(9003, IPAddr, fileCache[filename])
    
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
        print ("____________________")
        print msg
        print ("____________________")

        data = pickle.loads(msg)
        print "----------"
        for x in data:
            print x
            if(x[5] == "add"):
                print "adding files -->"+ IPAddr +"-->fileName-->"+ x[0]
                childNodes[IPAddr].fileMap[x[0]] = File(x[0], x[1], x[2], x[3], x[4])
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
        data, addr = sNode.recvfrom(1024)
        if data != '':
            # print("____________"+data+"___________")
            # print("____________"+myIPAddr+"___________")
            # print("____________"+addr[0]+"___________")

            sNode.sendto(myIPAddr, addr)
            # if Node(addr[0], False) in childNodes:
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

def heartBeat():
    print 'Inside HeartBeat'
    isCheck = False
    while True:
        # TCP_IP = "10.196.700.181"
        for x in list(childNodes):
            child = childNodes[x]
            if(child.liveStatus):
                print "Child IP : "+child.IPAddr
                TCP_IP = child.IPAddr
                TCP_PORT = 12121
                BUFFER_SIZE  = 1024
                tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
                tcpsock.bind((myIPAddr, TCP_PORT))
                tcpsock.settimeout(10)
                isCheck = True
                try:
                    tcpsock.listen(5)
                    print "Checking for Node Alive "+ TCP_IP
                    (conn, (ip, port)) = tcpsock.accept()
                    msg = conn.recv(1024)
                except socket.timeout as e:
                    # child.liveStatus = False
                    # print "Node is Dead AF : " + TCP_IP
                    tcpsock.close()
                    continue
                print "Node is Alive :) " + TCP_IP
                tcpsock.close()
        if isCheck:
            time.sleep(300)
            isCheck = False

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


    threads.append(setSuper)
    threads.append(t1)
    threads.append(hbt)
    threads.append(reqH)
    # starting threads 

    setSuper.start()
    t1.start()
    hbt.start()
    # sts.start()
    reqH.start()

    # wait until all threads finish 
    setSuper.join()
    t1.join()
    hbt.join()
    reqH.join()
