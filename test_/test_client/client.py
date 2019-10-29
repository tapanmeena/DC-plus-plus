# livestatus port number : 12121
# broadcasting port number : 44444
# addFile() sharing port : 44445
# supernode to supernode communication PORT : 9999
# filelist listen from supernode on PORT 9001
# filename send to supernode on PORT 9002
# ipaddress for file downloading on PORT 9003
# Request Handler running on Port 9090
# File sharing between Server and Client on PORT 9010
# ACK to supernode for assigning SuperNode 8090

import os, sys, socket, time, csv, pickle, subprocess
from threading import Thread
from SocketServer import ThreadingMixIn

PORT_fileSharing = 9010
PORT_filePre = 9111
PORT_filePost = 9112

IP_supernode = ''
numChunks = 4
BUFFER_SIZE = 1024

myIPaddr = ""

def myIP():
    global myIPaddr
    bashCommand = "hostname -I | awk '{print $1}'"
    myIPaddr = subprocess.check_output(['bash','-c', bashCommand])
    myIPaddr = myIPaddr.split('\n')
    myIPaddr = myIPaddr[0]

#--------------------Server-------------------------------
def server():
    global PORT_fileSharing
    print "in server--> ",myIPaddr, PORT_fileSharing

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
                # postTrans(filename)
                f.close()
                self.sock.close()
                break

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
        self.__numchunks = numChunks
        # Size of each chunk
        self.__chunksize = 0
        # Optional postfix string for the chunk filename
        self.__postfix = ''
        # Program name
        self.__progname = "FileSplitter.py"
        
    def doWork(self, fileName, action):
        self.__numchunks = int(numChunks)
        self.__filename = fileName
        print("---------action------->", action)
        if not self.__filename:
            sys.exit("Error: filename not given")
            return
        if action == 'split':
            self.split()
        elif action =='join':
            print "in join portion", fileName
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
        broadcast.close()
        if data is not None:
            IP_supernode = str(data)
            print "-------> ",data,"<__"
            print "--->",addr[0],"<--"
            IP_supernode = IP_supernode.strip('\n')
            time.sleep(1)
            
            sendMsgUDP(8090, addr[0], "ACK") #sedning ACK

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
            return ipList, tempList[itemNumber-1]
            # exit(1001)
            #another shit
        elif option == "R":
            #go back to main list
            tempList = fileList
            #do whatever you want to do
        else:
            print "\n\n\t\t \033[1m \033[91m Invalid Character Entered.. Try Again \033[0m"

def preTrans():
    #break the file into numchunks
    global myIPaddr, PORT_filePre

    BUFFER_SIZE = 1024
    tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print "------ in pre trans ---->????", myIPaddr, PORT_filePre

    tcpsock.bind((myIPaddr, PORT_filePre))

    while True:
        tcpsock.listen(5)
        print "Waiting for incoming connections..PRETRANS."
        (conn, (ip,port)) = tcpsock.accept()
        print 'Got connection from ', (ip,port)
        
        data = conn.recv(1024)
        msg = pickle.loads(data)

        print "pretrans file ->", msg
        fsp = FileSplitter()
        if(msg !=''):
            fsp.doWork(msg, 'split')

def postTrans():
    #delete the additional temporary chunks created for transfer

    global myIPaddr, PORT_filePost

    BUFFER_SIZE = 1024
    tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print "------ in post trans ---->????", myIPaddr, PORT_filePost
    tcpsock.bind((myIPaddr, PORT_filePost))
 
    while True:
        tcpsock.listen(5)
        print "Waiting for incoming connections..."
        (conn, (ip,port)) = tcpsock.accept()
        print 'Got connection from ', (ip,port)
        data = conn.recv(1024)
        msg = pickle.loads(data)

        fsp = FileSplitter()
        if(msg !=''):
            for x in range(1, numChunks+1):
                print("posttrnas", x)
                bashCommand = "rm "+str(msg)+"-"+str(x)
                myIPaddr = subprocess.check_output(['bash','-c', bashCommand])

def sharing(ipList, requestedFile, port):
    if ipList is None:
        return
    #for sending filename and receiving File from server(sender)
    TCP_IP = ipList[0] #sender ip address
    TCP_PORT = port
    BUFFER_SIZE = 1024

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    filename = str(requestedFile)
    s.send(filename)
    with open(filename, 'wb') as f:
        print 'file opened'
        while True:
            #print('receiving data...')
            data = s.recv(BUFFER_SIZE)
            # print "-----id-->", id
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

    myIP()

    #for Initial SuperNode assigning
    superNodeAssign()
    #For Checking Node Status

    serverT = Thread(target = server, name='serverT')
    serverT.start()


    prepFileT = Thread(target = preTrans,name ='prepFileT')
    postFileT = Thread(target = postTrans, name = 'postFileT')
    prepFileT.start()
    postFileT.start()

    alive = Thread(target = aliveChecker, name = 'alive')
    alive.start()

    while True:
        print("Press G to get Available File Names on Network")
        inputedValue = raw_input("Enter Character : ")
        if inputedValue == 'G':
            sendMsgUDP(9090, IP_supernode, 'showFiles')
            ipList, requestedFile = fileRequest()
            
            print "requested file_->", requestedFile

            #split file into chunks for parallel transfer
            sendObj(PORT_filePre, ipList[0], requestedFile)
            time_start = time.time()

            fst1 = Thread(target = sharing, args =(ipList, str(requestedFile)+'-1', 9010), name = 'fst1')
            fst2 = Thread(target = sharing, args =(ipList, str(requestedFile)+'-2', 9010), name = 'fst2')
            fst3 = Thread(target = sharing, args =(ipList, str(requestedFile)+'-3', 9010), name = 'fst3')
            fst4 = Thread(target = sharing, args =(ipList, str(requestedFile)+'-4', 9010), name = 'fst4')

            fst1.start()   
            fst2.start()
            fst3.start()
            fst4.start()
            
            fst1.join()
            fst2.join()
            fst3.join()
            fst4.join()
            
            fsp = FileSplitter()
            fsp.doWork(requestedFile, 'join')

            time_end = time.time()

            print "multi-part time ->", time_end-time_start

            # delete the temp chunks
            # sendObj(PORT_filePost, ipList[0], requestedFile)

           
            
           

            # sharing(ipList, requestedFile, 9010)
        else:
            print "\n\n\t\t \033[1m \033[91m Invalid Character Entered.. Try Again \033[0m"
    #for file sharing between sender and receiver
    # sharing()

############
#TODO TIME STAMP COMPARISION IN SEND NEW FILES TO SUPERNODE
############