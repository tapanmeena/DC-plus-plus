# broadcasting port number : 44444
# livestatus port number : 12121
# addFile() sharing port : 9005

import socket
import subprocess
import threading
import os
import time
import pickle

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

def addFiles(IPAddr):
    TCP_IP = IPAddr
    TCP_PORT = 9005
    BUFFER_SIZE  = 1024
    tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    tcpsock.bind((TCP_IP, TCP_PORT))
    tcpsock.settimeout(10) 
    try:
        tcpsock.listen(5)
        print "adding files -->"+ TCP_IP
        (conn, (ip, port)) = tcpsock.accept()
        msg = conn.recv(1024)
        data = pickle.loads(msg)
        print "----------"
        # x[0] -> file name
        # x[1]-x[4]-> file hashes
        for x in data:
            print x
            childNodes[IPAddr].fileMap[x[0]] = File(x[0], x[1], x[2], x[3], x[4])
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
                addFiles(addr[0])
            else:
                childNodes[addr[0]]=(Node(addr[0], True))
                print('------adding new node ----------')
                #TODO 
                addFiles(addr[0])

def heartBeat():
    print 'Inside HeartBeat'
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
        time.sleep(300)
                
if __name__ ==  "__main__": 
    
    threads = []
    # print ID of current process 
    # print("ID of process running main program: {}".format(os.getpid())) 
  
    # print name of main thread 
    # print("Main thread name: {}".format(threading.main_thread().name)) 

    # creating threads 
    t1 = threading.Thread(target=assignSuperNode, name='t1')
    # print 'after assigning'
    hbt = threading.Thread(target = heartBeat, name = 'heartBeat')

    threads.append(t1)
    threads.append(hbt)
    # starting threads 
    t1.start()
    hbt.start()
    # wait until all threads finish 
    t1.join()
    hbt.join()