import socket, time
from threading import Thread
from SocketServer import ThreadingMixIn
'''
TCP_IP = 'localhost'
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
'''
TCP_IP = '10.196.7.142'
TCP_PORT = 12121
BUFFER_SIZE  = 1024
tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
tcpsock.bind((TCP_IP, TCP_PORT))
tcpsock.settimeout(5)

try:
	tcpsock.listen(5)

	print "Checking for Node Alive "+ TCP_IP

	(conn, (ip, port)) = tcpsock.accept()
	msg = conn.recv(1024)
except socket.timeout as e:
	print e
if msg != "Alive":
    child.liveStatus = False
    print "Node is Dead AF : "+ ip
else:
	print "Node is Alive :) " + ip
tcpsock.close()