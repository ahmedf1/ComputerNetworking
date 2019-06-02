
#import socket module
from socket import *
import sys  # In order to terminate the program

serverSocket = socket(AF_INET, SOCK_STREAM) #Prepare a server socket
#Fill in start
serverPort = 1080
serverSocket.bind(('',serverPort))
serverSocket.listen(5)
#Fill in end


while True:
#Establish the connection
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    try:
    
        message = connectionSocket.recv(1024)
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()
        print(outputdata)
        #Send one HTTP header line into socket
        connectionSocket.send(('\HTTP/1.1 200 OK Content-type:text/html\r\n\r').encode())
        #connectionSocket.send(outputdata.encode())


        #Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
           connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())

        connectionSocket.close()
    except IOError:
        #Send response message for file not found
        connectionSocket.send(('\HTTP/1.1 404 Not Found\n\n').encode())
        #Close client socket
        connectionSocket.close()

serverSocket.close()
sys.exit()#Terminate the program after sending the corresponding data

