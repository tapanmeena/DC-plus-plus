#livestatus port number : 12121
#broadcasting port number : 44444
import socket, pickle
import time
import threading
import subprocess
#for sending filename and receiving File from server(sender)
TCP_IP = '10.250.1.93' #sender ip address
TCP_PORT = 9001
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
# filename = "1.deb"
filename = raw_input("Give File Name : ")
s.send(filename)
# start 
with open(filename, 'wb') as f:
    print 'file opened'
    start = time.time()
    while True:
        #print('receiving data...')
        data = s.recv(BUFFER_SIZE)
        # print('data=%s', (data))
        if not data:
            f.close()
            print 'file close()'
            break
        # write data to a file
        f.write(data)
    end = time.time()
print "Time Taken : ",end-start
print('Successfully get the file')
s.close()
print('connection closed')
'''
TCP_IP = 'localhost'
TCP_PORT = 12121    
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
msg = "Alive"
s.send(msg)
s.close()
print "I'm Alive BRO!!!"
time.sleep(100)
'''
# TCP_IP = '10.196.7.181'
# TCP_PORT = 12121
# BUFFER_SIZE  = 1024
# tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
# tcpsock.bind(("10.196.7.181", TCP_PORT))
# # tcpsock.settimeout(10)
# try:
#     tcpsock.listen(5)
#     print "Checking for Node Alive "+ TCP_IP
#     (conn, (ip, port)) = tcpsock.accept()
#     msg = conn.recv(1024)
# except socket.timeout as e:
#     print e
#     # child.liveStatus = False
#     print "Node is Dead AF : " + TCP_IP
#     tcpsock.close()
# print "Node is Alive :) " + TCP_IP
# tcpsock.close()
# function to recv an object via TCP socket
'''
import socket, pickle
def recvObj(port, IPAddr):
    TCP_IP = IPAddr
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
#function to send an object from TCP sockets
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

# fileList = recvObj(9001,'10.196.7.181')    
fileList = ['akas','ag','jydrstgr','asgf','efger','46sdf','asdf']
fileList.sort()
tempList = fileList
while True:
    i = 1
    print "\n"
    for item in tempList:
        print "\t", i, " -> ",item
        i += 1
    print "\n"
    print "#############################"
    print "\npress S to search any String\npress N for select Item number\npress R to return to Main List\n"
    print "#############################"
    option = raw_input("Enter Option here : ")
    if option == "S":
        #search a substring in filename List
        searchString = raw_input("Enter Search String : ")
        tempList = [s for s in tempList if searchString.lower() in s.lower()]
        # tempList.append("\n".join()
        # print "\n".join(s for s in fileList if searchString.lower() in s.lower())
        #someshit
    elif option == "N":
        #takes item number and returns filename to supernode for IP
        itemNumber = int(raw_input("Enter Item Number : "))
        print "Choosen File is : ",tempList[itemNumber-1]
        sendObj(9002,'10.196.7.181',tempList[itemNumber-1])
        exit(1001)
        #another shit
    elif option == "R":
        #go back to main list
        tempList = fileList
        #do whatever you want to do
    else:
        print "\n\n\t\t \033[1m \033[91m Invalid Character Entered.. Try Again \033[0m"
'''

# global ipAddr
# broadcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
# broadcast.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# Set a timeout so the socket does not block
# indefinitely when trying to receive data.
# broadcast.settimeout(5)
# broadcast.bind(("", 44444))

#to get it's own IP Address
# message = "Hi, I want to connect!!"
# while True:
#     broadcast.sendto(message, ('<broadcast>', 37020))
#     # print("message sent!")
#     data,addr = broadcast.recvfrom(1024)
#     if data is not None:
#         ipAddr = str(data)
#         ipAddr = ipAddr.strip('\n')
#         break
#     time.sleep(1)
# print "Super Node Ip Address : "+ str(ipAddr)

# def setSuperNodes():
    # accept requests to become superNode
# bashCommand = "hostname -I | awk '{print $1}'"
# myIPAddr = subprocess.check_output(['bash','-c', bashCommand])
# myIPAddr = myIPAddr.split('\n')
# superNodeList = []
# # print "___"+str(myIPAddr)+"__"
# sNode = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
# sNode.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# sNode.bind(("", 11000))

# while True:
#     # continuously listen for broadcast msgs
#     data, addr = sNode.recvfrom(1024)
#     print "Hello "
#     if data != '':
#         print "_______get superNodes _____"+data+"___________"
#         print "New Connected SuperNode ______"+addr[0]+"__"
#         if addr[0] not in superNodeList:
#             superNodeList.append(addr[0])
#         print superNodeList

# bashCommand = "hostname -I | awk '{print $1}'"
# myIPAddr = subprocess.check_output(['bash','-c', bashCommand])
# myIPAddr = myIPAddr.split('\n')
# myIPAddr = myIPAddr[0]
# print "____"+str(myIPAddr)+"___"

# def recvObj(port):
#     TCP_IP = myIPAddr
#     TCP_PORT = port
#     BUFFER_SIZE  = 1024
#     tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
#     tcpsock.bind((TCP_IP, TCP_PORT))
#     tcpsock.settimeout(10)
#     try:
#         tcpsock.listen(5)
#         (conn, (ip, port)) = tcpsock.accept()
#         msg = conn.recv(1024)
#         data = pickle.loads(msg)
#         tcpsock.close()
#         return data 

#     except socket.timeout as e:
#         print "files addition socket timeout : " + TCP_IP
#         tcpsock.close()
#         return
#     tcpsock.close()

# #function to send an object from TCP sockets
# def sendObj(port, IPAddr, obj):
#     TCP_IP = str(IPAddr)
#     TCP_PORT = port
#     BUFFER_SIZE = 1024

#     #convert object to serial stream  
#     msg = pickle.dumps(obj)
    
#     p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     try:
#         p.connect((str(TCP_IP), TCP_PORT))
#         p.send(msg)
#         p.close()
#     except socket.error , exc:
#         print "Error Caught : ",exc

# def findFile(IPAddr):
#     filename = recvObj(9002)
#     print "Filename  :",filename
#     sendObj(9003, IPAddr, 'someshit')

# sNode = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
# sNode.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# sNode.bind(("", 9090))
# # continuously listen for broadcast msgs
# data, addr = sNode.recvfrom(1024)
# findFile(addr[0])

'''
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
'''
'''
# livestatus port number : 12121
# broadcasting port number : 44444
# addFile() sharing port : 44445
# supernode to supernode communication PORT : 9999
# filelist listen from supernode on PORT 9001
# filename send to supernode on PORT 9002
# ipaddress for file downloading on PORT 9003
# Request Handler running on Port 9090
# File sharing between Server and Client on PORT 9010

import os, sys, socket, time, csv, pickle, subprocess
from threading import Thread
from SocketServer import ThreadingMixIn


PORT_fileSharing = 9010

IP_supernode = ''
numChunks = 4
BUFFER_SIZE = 1024

myIPaddr = ""

def myIP():
    global myIPaddr
    bashCommand = "hostname -I | awk '{print $1}'"
    myIPaddr = subprocess.check_output(['bash','-c', bashCommand])
    myIPaddr = myIPaddr.split('\n')

#--------------------Server-------------------------------
class ClientThread(Thread):
    def __init__(self,ip,port,sock):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        print " New thread started for "+ip+":"+str(port)

    def run(self):
        filename = self.sock.recv(BUFFER_SIZE)
        print "Filename Bitches : "+filename
        # filename='mytext.txt'
        f = open(filename,'rb')
        while True:
            l = f.read(BUFFER_SIZE)
            while (l):
                self.sock.send(l)
                # print('Sent ',repr(l))
                l = f.read(BUFFER_SIZE)
            if not l:
                f.close()
                self.sock.close()
                break

def server():
    global PORT_fileSharing
    print "haramkhor ",PORT_fileSharing

    # bashCommand = "hostname -I | awk '{print $1}'"
    # IPAddr = subprocess.check_output(['bash','-c', bashCommand])
    # IPAddr = IPAddr.strip("\n")

    BUFFER_SIZE = 1024
    tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcpsock.bind((myIPaddr, PORT_fileSharing))
    threads = []

    while True:
        tcpsock.listen(5)
        print "Waiting for incoming connections..."
        (conn, (ip,port)) = tcpsock.accept()
        print 'Got connection from ', (ip,port)
        newthread = ClientThread(ip,port,conn)
        newthread.start()
        threads.append(newthread)

    for t in threads:
        t.join()

#==================== server ends ========================

# --------------file splitting utility--------------------

class FileSplitterException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class FileSplitter:
    """ File splitter class """

    def __init__(self):

        # cache filename
        self.__filename = ''
        # number of equal sized chunks
        self.__numchunks = 4
        # Size of each chunk
        self.__chunksize = 0
        # Optional postfix string for the chunk filename
        self.__postfix = ''
        # Program name
        self.__progname = "FileSplitter.py"
        
    def doWork(self, fileName, action):
        self.__numchunks = int(numChunks)
        self.__filename = fileName
        if not self.__filename:
            sys.exit("Error: filename not given")
            return
        if action == 'split':
            self.split()
        elif action =='join':
            self.combine()
        
    def split(self):
        """ Split the file and save chunks
        to separate files """

        print 'Splitting file', self.__filename
        print 'Number of chunks', self.__numchunks, '\n'
        
        try:
            f = open(self.__filename, 'rb')
        except (OSError, IOError), e:
            raise FileSplitterException, str(e)

        bname = (os.path.split(self.__filename))[1]
        # Get the file size
        fsize = os.path.getsize(self.__filename)
        # Get size of each chunk
        self.__chunksize = int(float(fsize)/float(self.__numchunks))

        chunksz = self.__chunksize
        total_bytes = 0

        for x in range(self.__numchunks):
            chunkfilename = bname + '-' + str(x+1) + self.__postfix

            # if reading the last section, calculate correct
            # chunk size.
            if x == self.__numchunks - 1:
                chunksz = fsize - total_bytes

            try:
                print 'Writing file',chunkfilename
                data = f.read(chunksz)
                total_bytes += len(data)
                chunkf = file(chunkfilename, 'wb')
                chunkf.write(data)
                chunkf.close()
            except (OSError, IOError), e:
                print e
                continue
            except EOFError, e:
                print e
                break

        print 'Done.'

    def sort_index(self, f1, f2):

        index1 = f1.rfind('-')
        index2 = f2.rfind('-')
        
        if index1 != -1 and index2 != -1:
            i1 = int(f1[index1:len(f1)])
            i2 = int(f2[index2:len(f2)])
            return i2 - i1
        
    def combine(self):
        """ Combine existing chunks to recreate the file.
        The chunks must be present in the cwd. The new file
        will be written to cwd. """

        import re
        
        print 'Creating file', self.__filename
        
        bname = (os.path.split(self.__filename))[1]
        bname2 = bname
        
        # bugfix: if file contains characters like +,.,[]
        # properly escape them, otherwise re will fail to match.
        for a, b in zip(['+', '.', '[', ']','$', '(', ')'],
                        ['\+','\.','\[','\]','\$', '\(', '\)']):
            bname2 = bname2.replace(a, b)
            
        chunkre = re.compile(bname2 + '-' + '[0-9]+')
        
        chunkfiles = []
        for f in os.listdir("."):
            print f
            if chunkre.match(f):
                chunkfiles.append(f)


        print 'Number of chunks', len(chunkfiles), '\n'
        chunkfiles.sort(self.sort_index)

        data=''
        for f in chunkfiles:

            try:
                print 'Appending chunk', os.path.join(".", f)
                data += open(f, 'rb').read()
            except (OSError, IOError, EOFError), e:
                print e
                continue

        try:
            f = open(bname, 'wb')
            f.write(data)
            f.close()
        except (OSError, IOError, EOFError), e:
            raise FileSplitterException, str(e)

        print 'Wrote file', bname

#--------------------------------------------------------- 

#function to receive an object from TCP sockets
def recvObj(port):
    TCP_IP = myIPaddr
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

#function to send an object from TCP sockets
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

def aliveChecker():
    time.sleep(8)
    while True:
        TCP_IP = myIPaddr
        TCP_PORT = 12121
        BUFFER_SIZE = 1024
        # print "TCP->" + TCP_IP

        p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            p.connect((TCP_IP, TCP_PORT))
            msg = "Alive"
            print msg
            p.send(msg)
            p.close()
            print "I'm Alive BRO!!!"
            time.sleep(100)
        except socket.error , exc:
            # print "Error Caught : ",exc
            time.sleep(20)

def superNodeAssign():
    global IP_supernode
    broadcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    broadcast.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Set a timeout so the socket does not block
    # indefinitely when trying to receive data.
    broadcast.settimeout(5)
    broadcast.bind(("", 44444))

    #to get it's own IP Address
    # bashCommand = "hostname -I | awk '{print $1}'"
    # message = subprocess.check_output(['bash','-c', bashCommand])
    message = "Hi, I want to connect!!"
    while True:
        broadcast.sendto(message, ('<broadcast>', 37020))
        # print("message sent!")
        data,addr = broadcast.recvfrom(1024)
        if data is not None:
            IP_supernode = str(data)
            print "-------> ",data,"<__"
            print "--->",addr[0],"<--"
            IP_supernode = IP_supernode.strip('\n')
            break
        time.sleep(1)
    print "Super Node Ip Address : "+ str(IP_supernode)
    listFiles()

#assumption a list of fileName is coming
def fileRequest():
    fileList = recvObj(9001)
    # fileList = ['akas','ag','jydrstgr','asgf','efger','46sdf','asdf']
    fileList.sort()
    tempList = fileList
    while True:
        i = 1
        print "\n"
        for item in tempList:
            print "\t", i, " -> ",item
            i += 1
        print "\n"
        print "#############################"
        print "\npress S to search any String\npress N for select Item number\npress R to return to Main List\n"
        print "#############################"
        option = raw_input("Enter Option here : ")
        if option == "S":
            #search a substring in filename List
            searchString = raw_input("Enter Search String : ")
            tempList = [s for s in tempList if searchString.lower() in s.lower()]
            # tempList.append("\n".join()
            # print "\n".join(s for s in fileList if searchString.lower() in s.lower())
            #someshit
        elif option == "N":
            #takes item number and returns filename to supernode for IP
            itemNumber = int(raw_input("Enter Item Number : "))
            print "Choosen File is : ",tempList[itemNumber-1]
            sendMsgUDP(9090, IP_supernode, 'findFile')
            time.sleep(1)
            sendObj(9002,IP_supernode, tempList[itemNumber-1])
            ipList = recvObj(9003)
            return ipList
            # exit(1001)
            #another shit
        elif option == "R":
            #go back to main list
            tempList = fileList
            #do whatever you want to do
        else:
            print "\n\n\t\t \033[1m \033[91m Invalid Character Entered.. Try Again \033[0m"

def sharing(ipList):
    if ipList is None:
        return
    #for sending filename and receiving File from server(sender)
    TCP_IP = ipList[0] #sender ip address
    TCP_PORT = 9010
    BUFFER_SIZE = 1024

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    filename = raw_input("Give File Name : ")
    s.send(filename)
    with open(filename, 'wb') as f:
        print 'file opened'
        while True:
            #print('receiving data...')
            data = s.recv(BUFFER_SIZE)
            # print('data=%s', (data))
            if not data:
                f.close()
                print 'file close()'
                break
            # write data to a file
            f.write(data)

    print('Successfully get the file')
    s.close()
    print('connection closed')

def computeHash(filename):
    hashList = []
    for i in range(1,numChunks+1):
        bashcommand = "md5sum "+str(filename)+"-"+str(i)
        Hash = subprocess.check_output(['bash','-c', bashcommand])
        Hash = Hash.split(' ')
        hashList.append(Hash[0])
    return hashList

def dumpContent(filename):
    fileContent = []
    with open(filename, 'rb') as f:
        reader = csv.reader(f)

        # read file row by row
        for row in reader:
            fileContent.append(row)

    return fileContent

def removeSplittedFiles(filename):
    command = "rm "+str(filename)+"-*"
    os.system(command)

def Diff(li1, li2):
    li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2] 
    return li_dif
    # return (list(set(list1) - set(list2)))

def listFiles():
    filename = 'listFiles.csv'
    fileDump = []
    fileExist = False
    if(os.path.exists(filename)):
        fileExist = True

    bashCommand = "ls -l | awk '{print $6, $7, $8, $9}'"
    fileList = subprocess.check_output(['bash','-c', bashCommand])
    fileList = fileList.split('\n')
    numFiles = len(fileList)

    if not fileExist:
        with open(filename, 'wb') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for i in range(1, numFiles-1):
                item = fileList[i].split(' ')
                date = str(item[0]) + str(item[1])
                time =  str(item[2])
                fileName = str(item[3])
                fsp = FileSplitter()
                fsp.doWork(fileName, 'split')
                hashes = computeHash(fileName)

                removeSplittedFiles(fileName)
                # print hashes
                filewriter.writerow([fileName, hashes[0], hashes[1], hashes[2], hashes[3],"add", date, time])
                fileDump.append([fileName, hashes[0], hashes[1], hashes[2], hashes[3], date, time])
    else:
        print("-------> If List Files Exist <-------")
        originalFileContent = dumpContent(filename)
        # fileDump = []
        print originalFileContent
        os.remove('listFiles.csv')
        fileNameList = []
        newFileNameList = []
        timeStampList = []
        dateStampList = []
        hashesList = []
        with open(filename, 'wb') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)

            for fileN in originalFileContent:
                fileNameList.append(fileN[0])
                hashesList.append([fileN[1], fileN[2], fileN[3], fileN[4]])
                dateStampList.append(fileN[5])
                timeStampList.append(fileN[6])

            for i in range(1,numFiles-1):
                item = fileList[i].split(' ')
                date = str(item[0]) + str(item[1])
                time = str(item[2])
                fileN = str(item[3])
                newFileNameList.append(fileN)

                #check if file exist and its time stamp with recorded LOG
                if(fileN in fileNameList):
                    index = fileNameList.index(fileN)
                    #checking if timestamp are same or not
                    print "###############################"
                    print "File Name :" + fileN
                    
                    if dateStampList[index] < date:
                        print dateStampList[index] + date
                        # print "gandu"
                        fsp = FileSplitter()
                        fsp.doWork(fileN, 'split')
                        hashes = computeHash(fileN)
                        filewriter.writerow([fileN, hashes[0], hashes[1], hashes[2], hashes[3],"add", date, time])
                        fileDump.append([fileN, hashes[0], hashes[1], hashes[2], hashes[3], date, time])
                        removeSplittedFiles(fileN)

                    elif dateStampList[index] == date:
                        if timeStampList[index] < time:
                            print timeStampList[index] + time
                            fsp = FileSplitter()
                            fsp.doWork(fileN, 'split')
                            hashes = computeHash(fileN)
                            filewriter.writerow([fileN, hashes[0], hashes[1], hashes[2], hashes[3],"add", date, time])
                            fileDump.append([fileN, hashes[0], hashes[1], hashes[2], hashes[3], date, time])
                            removeSplittedFiles(fileN)
                        else:
                            fileDump.append([fileN, hashesList[index][0], hashesList[index][1], hashesList[index][2], hashesList[index][3], date, time])
                    else:
                        fileDump.append([fileN, hashesList[index][0], hashesList[index][1], hashesList[index][2], hashesList[index][3], date, time])
                else:
                    print "File Not Present"
                    fsp = FileSplitter()
                    fsp.doWork(fileN, 'split')
                    hashes = computeHash(fileN)
                    filewriter.writerow([fileN, hashes[0], hashes[1], hashes[2], hashes[3],"add", date, time])
                    fileDump.append([fileN, hashes[0], hashes[1], hashes[2], hashes[3], date, time])
                    removeSplittedFiles(fileN)

            ## Get filename that need to be delete from SuperNode
            fileNotNeeded = Diff(fileNameList, newFileNameList)
            print  "--------------------------------"
            print fileNotNeeded
            print  "--------------------------------"
            for names in fileNotNeeded:
                filewriter.writerow([names,'0','0','0','0',"delete",'0','0'])
    fileContents = dumpContent('listFiles.csv')
    print fileContents

    os.remove('listFiles.csv')
    # print "--> printing file Dump <--"
    # print fileDump
    with open('listFiles.csv', 'wb') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for i in fileDump:
            filewriter.writerow(i)

    # sending csv file to supernode
    msg = pickle.dumps(fileContents)
    print "Message ---> "+msg
    TCP_IP = IP_supernode
    TCP_PORT = 44445
    BUFFER_SIZE = 5096
    print "TCP->" + TCP_IP,"<--"

    p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    p.connect((str(TCP_IP), TCP_PORT))
    p.send(msg)
    p.close()
    print "__Updated File List Sent__"
    return

def sendMsgUDP(port, ip, msg):
    serverAddrPort = (ip, port) 
    UDPClientSocket = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM)   
    UDPClientSocket.sendto(msg, serverAddrPort)
    UDPClientSocket.close()
      
if __name__ == '__main__':
    #for Initial SuperNode assigning
    superNodeAssign()
    #For Checking Node Status

    serverT = Thread(target = server, name='serverT')
    serverT.start()

    alive = Thread(target = aliveChecker, name = 'alive')
    alive.start()

    while True:
        print("Press G to get Available File Names on Network")
        inputedValue = raw_input("Enter Character : ")
        if inputedValue == 'G':
            sendMsgUDP(9090, IP_supernode, 'showFiles')
            ipList = fileRequest()
            sharing(ipList)
        else:
            print "\n\n\t\t \033[1m \033[91m Invalid Character Entered.. Try Again \033[0m"
    #for file sharing between sender and receiver
    # sharing()

############
#TODO TIME STAMP COMPARISION IN SEND NEW FILES TO SUPERNODE
############
'''