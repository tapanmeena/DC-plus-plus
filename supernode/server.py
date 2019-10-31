import socket, time, subprocess,pickle
from threading import Thread
from SocketServer import ThreadingMixIn
# '''
TCP_IP = '10.250.1.93'
TCP_PORT = 9001
BUFFER_SIZE = 1024

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

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((TCP_IP, TCP_PORT))
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
# '''
# '''
# TCP_IP = '10.196.7.142'
# TCP_PORT = 12121
# BUFFER_SIZE  = 1024
# tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
# tcpsock.bind((TCP_IP, TCP_PORT))
# tcpsock.settimeout(5)

# try:
# 	tcpsock.listen(5)

# 	print "Checking for Node Alive "+ TCP_IP

# 	(conn, (ip, port)) = tcpsock.accept()
# 	msg = conn.recv(1024)
# except socket.timeout as e:
# 	print e
# if msg != "Alive":
#     child.liveStatus = False
#     print "Node is Dead AF : "+ ip
# else:
# 	print "Node is Alive :) " + ip
# tcpsock.close()
# '''
# # while True:
# #     TCP_IP = '10.196.7.181'
# #     # some_IP = 'localhost'
# #     TCP_PORT = 12121    
# #     BUFFER_SIZE = 1024
# #     print "TCP " +TCP_IP

# #     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# #     s.connect(("10.196.7.181", TCP_PORT))
# #     msg = "Alive"
# #     print msg
# #     s.send(msg)
# #     s.close()
# #     print "I'm Alive BRO!!!"
# #     time.sleep(100) 
# import subprocess
# # filename = 'client.py'
# # hashList = []
# # for i in range(1,4+1):
# #     bashcommand = "md5sum "+str(filename)
# #     Hash = subprocess.check_output(['bash','-c', bashcommand])
# #     Hash = Hash.split(' ')
# #     print Hash[0]
# #     hashList.append(Hash[0])
# # print(hashList)
# # bashCommand = "ls -l | awk '{print $6, $7, $8, $9 }'"
# # fileList = subprocess.check_output(['bash','-c', bashCommand])
# # fileList = fileList.split('\n')
# # numFiles = len(fileList)
# # for i in range(1, numFiles-1):
# #     item = fileList[i].split(' ')
# #     timeStamp = str(item[0]) + str(item[1]) + str(item[2])
# #     fileName = str(item[3])
# #     print fileName
# # import os
# # filename = "abcd"
# # command = "rm "+str(filename)+"-*"
# # os.system(command)
# supernodeIPList = ['10.196.7.181']
# class Node:
#     def __init__(self, IPAddr, liveStatus) :
#         self.IPAddr = IPAddr
#         self.liveStatus = liveStatus
#         self.fileMap = {}
#     def __eq__(self, other):
#         if not isinstance(other, Node):
#             # don't attempt to compare against unrelated types
#             return NotImplemented
#         return self.IPAddr == other.IPAddr

# class File: 
#     def __init__(self, name, h1, h2, h3, h4):
#         self.name = name`
#         self.h1 = h1
#         self.h2 = h2
#         self.h3 = h3
#         self.h4 = h4

# # containing objects of Node
# childNodes = {} #{IPAddr->Node}
# IPAddr = '10.196.7.181'
# childNodes[IPAddr].fileMap['1'] = File('1', '2', '3', '4', '5')
# childNodes[IPAddr].fileMap['2'] = File('2', '2', '3', '4', '5')
# childNodes[IPAddr].fileMap['3'] = File('3', '2', '3', '4', '5')

# function to recv an object via TCP socket
'''
def recvObj(port, IPAddr):
    TCP_IP = IPAddr
    TCP_PORT = port
    BUFFER_SIZE  = 1024
    tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    tcpsock.bind((TCP_IP, TCP_PORT))
    tcpsock.settimeout(100) 
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

def showFile():
    result = []
    fileCache = ['123','ag','jydrstgr','asgf','efger','46sdf','asdf']
    for x in fileCache:
        result.append(x)
    sendObj(9001, "10.196.7.181", result)
    filename = recvObj(9002, "10.196.7.181")
    print filename
showFile()
'''
# bashCommand = "hostname -I | awk '{print $1}'"
# IPAddr = subprocess.check_output(['bash','-c', bashCommand])
# sNode = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
# sNode.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# sNode.bind(("", 37020))
# while True:
#     # continuously listen for broadcast msgs
#     data, addr = sNode.recvfrom(1024)
#     if data != '':
#         sNode.sendto(IPAddr, addr)
#         print "TU mc ",data


# import socket
# import subprocess
# import threading
# import os

# children = []

# def assignSuperNode():
#     # accept requests to become superNode
#     bashCommand = 'hostname -I | awk \'{print $1}\''
#     IPAddr = subprocess.check_output(['bash','-c', bashCommand])
#     sNode = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
#     sNode.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
#     sNode.bind(("", 37020))
#     while True:
#         # continuously listen for broadcast msgs
#         data, addr = sNode.recvfrom(1024)
#         if data != '':
#             print data


# if __name__ ==  "__main__": 
    
#     # print ID of current process 
#     print("ID of process running main program: {}".format(os.getpid())) 
  
#     # print name of main thread 
#     # print("Main thread name: {}".format(threading.main_thread().name)) 
  
#     # creating threads 
#     t1 = threading.Thread(target=assignSuperNode, name='t1')  
  
#     # starting threads 
#     t1.start()

#     # wait until all threads finish 
#     t1.join() 
#function to receive an object from TCP sockets

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

# serverAddrPort = ("", 9090) 
# UDPClientSocket = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM)   
# UDPClientSocket.sendto('findFile', serverAddrPort)   

# sendObj(9002,myIPAddr, 1)
# ipList = recvObj(9003)