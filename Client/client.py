#livestatus port number : 12121
#broadcasting port number : 44444
import socket
import time
import threading

ipAddr = ""

def aliveChecker():
    while True:
        TCP_IP = ipAddr
        TCP_PORT = 12121    
        BUFFER_SIZE = 1024
        print "TCP "+TCP_IP

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
        msg = "Alive"
        print msg
        s.send(msg)
        s.close()
        print "I'm Alive BRO!!!"
        time.sleep(100) 

def superNodeAssign():
    global ipAddr
    broadcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    broadcast.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Set a timeout so the socket does not block
    # indefinitely when trying to receive data.
    broadcast.settimeout(0.2)
    broadcast.bind(("", 44444))

    #to get it's own IP Address
    # bashCommand = "hostname -I | awk '{print $1}'"
    # message = subprocess.check_output(['bash','-c', bashCommand])
    message = "Hi, I want to connect!!"
    while True:
        broadcast.sendto(message, ('<broadcast>', 37020))
        print("message sent!")
        data,addr = broadcast.recvfrom(1024)
        if data is not None:
            ipAddr = str(data)
            break
        time.sleep(1)
    print "Super Node Ip Address : "+ str(ipAddr)

def sharing():
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

if __name__ == '__main__':
    #for Initial SuperNode assigning
    superNodeAssign()
    #For Checking Node Status
    # ipAddr = "10.196.7.142"
    alive = threading.Thread(target = aliveChecker, name = 'alive')
    alive.start()


    #for file sharing between sender and receiver
    # sharing()