from socket import *
import os
import sys
import struct
import time
import select
import binascii


ICMP_ECHO_REQUEST = 8
MAX_HOPS = 30
TIMEOUT = 2.0
TRIES = 2
pid = os.getpid() & 0xffff

# The packet that we shall send to each router along the path is the ICMP echo
# request packet, which is exactly what we had used in the ICMP ping exercise. # We shall use the same packet that we built in the Ping exercise
def checksum(string):
# In this function we make the checksum of our packet
# hint: see icmpPing lab
    csum = 0
    countTo = (len(string) // 2) * 2
    count = 0

    while count < countTo:
        thisVal = ord(string[count+1]) * 256 + ord(string[count])
        csum = csum + thisVal
        csum = csum & 0xffffffff
        count = count + 2

    if countTo < len(string):
        csum = csum + ord(string[len(string) - 1])
        csum = csum & 0xfffffffff

    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer



def build_packet():
    csum = 0
    header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0, csum, pid, 1)
    data = struct.pack('d', time.time())
    
    csum = checksum(header + data)          

    if sys.platform == 'darwin':         
        csum = htons(csum) & 0xffff            
    else:         
        csum = htons(csum)              

    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, csum, pid, 1)     
    packet = header + data
    return packet



def get_route(hostname):
    timeLeft = TIMEOUT
    for ttl in range(1,MAX_HOPS):
        for tries in range(TRIES):
            destAddr = gethostbyname(hostname)
            #Fill in start
            # Make a raw socket named mySocket
            mySocket = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP)
            #Fill in end
            mySocket.setsockopt(IPPROTO_IP, IP_TTL, struct.pack('I', ttl))
            mySocket.settimeout(TIMEOUT)

            try:
                d = build_packet()
                mySocket.sendto(d, (hostname, 0))
                t= time.time()
                startedSelect = time.time()
                whatReady = select.select([mySocket], [], [], timeLeft)
                howLongInSelect = (time.time() - startedSelect)
                
                if whatReady[0] == []: # Timeout
                    print(" * * * Request timed out.")

                recvPacket, addr = mySocket.recvfrom(1024)
                timeReceived = time.time()
                timeLeft = timeLeft - howLongInSelect

                if timeLeft <= 0:
                    print("  *        *        *    Request timed out.")

            except timeout:
                continue
            
            else:

                #Fill in start
                #Fetch the icmp type from the IP packet
                type, = struct.unpack('b', recvPacket[20:21])
                #Fill in end
                
                if type == 11:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    print(" %d         rtt=%.0f ms      %s" % (ttl,(timeReceived-t)*1000, addr[0]))
                elif type == 3:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    print(" %d         rtt=%.0f ms      %s" % (ttl,(timeReceived-t)*1000, addr[0]))
                elif type == 0:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    print(" %d         rtt=%.0f ms      %s" % (ttl,(timeReceived-t)*1000, addr[0]))
                else:
                    print("error")
                break

            finally:
                mySocket.close()
                

get_route("google.com")
#get_route("yahoo.com")
#get_route("bing.com")
#get_route("youtube.com")
