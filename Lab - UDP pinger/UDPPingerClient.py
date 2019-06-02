import time
import sys
from socket import *

    
# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
clientSocket = socket(AF_INET, SOCK_DGRAM)

# set a timeout so it doesn't wait forever
clientSocket.settimeout(1)

# Get server ip and port number
remoteAddress = (sys.argv[1], int(sys.argv[2]))

# 10 pings
for i in range(10):
    
    timeSent = time.time()
    msg = 'PING ' + str(i + 1) + " " + str(time.strftime("%H:%M:%S"))
    clientSocket.sendto(msg, remoteAddress)
    
    try:
        data, server = clientSocket.recvfrom(1024)
        timeReceived = time.time()
        rtt = timeReceived - timeSent
        print "Message Received", data
        print "Round Trip Time", rtt
        print
    
    except timeout:
        print 'REQUEST TIMED OUT'
        print
