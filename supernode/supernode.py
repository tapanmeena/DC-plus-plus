# broadcasting port number : 44444
# livestatus port number : 12121
# handleFile() sharing port : 9005
# supernode to supernode communication PORT : 9999

import socket
import subprocess
import threading
import os
import time
import pickle
from collections import defaultdict
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

# returns the list of all filenames from alive nodes.
def showFile():
    result = []
    for x in fileCache:
        if(len)

# gets filename and returns list of IP
def findFile():
    
def handleFiles(IPAddr):
    TCP_IP = IPAddr
    TCP_PORT = 9005
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
        print "----------"
        for x in data:
            print x
            if(x[5] == "add"):
                print "adding files -->"+ TCP_IP +"-->fileName-->"+ x[0]
                childNodes[IPAddr].fileMap[x[0]] = File(x[0], x[1], x[2], x[3], x[4])
                fileCache[x[0]].append(IPAddr)
            elif(x[5] == "delete"):
                print "deleting files -->"+ TCP_IP+"-->filename-->"+ x[0]
                del(childNodes[IPAddr].fileMap[x[0]])
                fileCache[x[0]].remove(IPAddr)

        print "----------"

        x = childNodes[IPAddr]
        for y in x.fileMap:
            print(x.fileMap[y].name)                     
    except socket.timeout as e:
        print "files addition socket timeout : " + TCP_IP
        tcpsock.close()
        return
    tcpsock.close()

def assignSuperNode():
    # accept requests to become superNode
    bashCommand = 'hostname -I | awk \'{print $1}\''
    IPAddr = subprocess.check_output(['bash','-c', bashCommand])
    sNode = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    sNode.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sNode.bind(("", 37020))
    while True:
        # continuously listen for broadcast msgs
        data, addr = sNode.recvfrom(1024)
        if data != '':
            sNode.sendto(IPAddr, addr)
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
        for x in childNodes:
            child = childNodes[x]
            if(child.liveStatus):
                print "Child IP : "+child.IPAddr
                TCP_IP = child.IPAddr
                TCP_PORT = 12121
                BUFFER_SIZE  = 1024
                tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
                tcpsock.bind((str(child.IPAddr), TCP_PORT))
                tcpsock.settimeout(10) 
                isCheck = True
                try:
                    tcpsock.listen(5)
                    print "Checking for Node Alive "+ TCP_IP
                    (conn, (ip, port)) = tcpsock.accept()
                    msg = conn.recv(1024)
                except socket.timeout as e:
                    child.liveStatus = False
                    print "Node is Dead AF : " + TCP_IP
                    tcpsock.close()
                    continue
                print "Node is Alive :) " + TCP_IP
                tcpsock.close()
        if isCheck:
            time.sleep(300)
            isCheck = False

def SupernodeToSupernode():
    supernodeIPList = ['10.196.7.181']
    
if __name__ ==  "__main__": 
    
    threads = []
    # print ID of current process 
    # print("ID of process running main program: {}".format(os.getpid())) 
  
    # print name of main thread 
    # print("Main thread name: {}".format(threading.main_thread().name)) 

    # Run forever to Assign Super node to Client
    t1 = threading.Thread(target=assignSuperNode, name='t1')

    # Run forever to check File Server Live Status (Alive/Dead)
    hbt = threading.Thread(target = heartBeat, name = 'heartBeat')

    #thread from supernode to supernode communication
    sts = threading.Thread(target = SupernodeToSupernode, name = 'sts')

    threads.append(t1)
    threads.append(hbt)
    threads.append(sts)
    # starting threads 
    t1.start()
    hbt.start()
    sts.start()
    # wait until all threads finish 
    t1.join()
    hbt.join()
    sts.join()