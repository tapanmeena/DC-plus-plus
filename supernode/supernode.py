#livestatus port number : 12121
#broadcasting port number : 44444
import socket
import subprocess
import threading
import os
import time

nFiles = 0
class Node:
    def __init__(self, IPAddr, liveStatus) :
        self.IPAddr = IPAddr
        self.liveStatus = liveStatus
    def __eq__(self, other):
        if not isinstance(other, Node):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.IPAddr == other.IPAddr and self.liveStatus == other.liveStatus

class File: 
    def __init__(self, name, h1, h2, h3, h4, liveStatus, IPAddr):
        self.id = nFiles
        self.name = name
        self.h1 = h1
        self.h2 = h2
        self.h3 = h3
        self.h4 = h4
        self.liveStatus = liveStatus
        self.IPAddr = IPAddr
        fileMap[id] = self
        nFiles += 1 

# containing objects of Node
childNodes = []
fileMap = {}
    

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
            if Node(addr[0], False) in childNodes:
                childNodes[childNodes.index(Node(addr[0], False))].liveStatus = True
                print('----------dead to alive-------')
                #TODO
                #pickle pass
                # updateFiles(data)
            else:
                childNodes.append(Node(addr[0], True))
                print('------adding new node ----------')
                #TODO 
                #pickle pass list as msg
                # addFiles(data)

def heartBeat():
    while True:
        for child in childNodes:
            print "Child IP : "+child.IPAddr
            if child.liveStatus:
                TCP_IP = child.IPAddr
                TCP_PORT = 12121
                BUFFER_SIZE  = 1024
                tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
                tcpsock.bind((TCP_IP, TCP_PORT))
                tcpsock.settimeout(10)
                try:
                    tcpsock.listen(5)
                    print "Checking for Node Alive "+ TCP_IP
                    (conn, (ip, port)) = tcpsock.accept()
                    msg = tcpsock.recv(1024)
                except socket.timeout as e:
                    child.liveStatus = False
                    print "Node is Dead AF : " + TCP_IP
                    tcpsock.close()
                    continue
                print "Node is Alive :) " + TCP_IP
                tcpsock.close()                
        time.sleep(10)

if __name__ ==  "__main__": 
    
    threads = []
    # print ID of current process 
    # print("ID of process running main program: {}".format(os.getpid())) 
  
    # print name of main thread 
    # print("Main thread name: {}".format(threading.main_thread().name)) 

    # creating threads 
    t1 = threading.Thread(target=assignSuperNode, name='t1')  
    hbt = threading.Thread(target = heartBeat, name = 'heartBeat')

    threads.append(t1)
    threads.append(hbt)
    # starting threads 
    t1.start()
    hbt.start()
    # wait until all threads finish 
    t1.join()
    hbt.join()