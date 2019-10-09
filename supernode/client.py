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
