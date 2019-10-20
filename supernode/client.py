#livestatus port number : 12121
#broadcasting port number : 44444
import socket
import time
import threading

'''
#for sending filename and receiving File from server(sender)
TCP_IP = 'localhost' #sender ip address
TCP_PORT = 9001
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
'''
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
fileList = ['akas','ag','jydrstgr','asgf','efger','46sdf','asdf']
fileList.sort()
tempList = []
while True:
    i = 1
    fileList
    for item in fileList:
        print i, item
        i += 1
    print "#############################"
    print "\npress S to search any String\npress N for select Item number\npress R to return to Main List\n"
    print "#############################"
    break