__author__ = 'Jan Kempeneers'

import os


'''
do this once
    create server
    open socket
    get current screen resolution 
    calculate ratio in x (ScreenWidth) and y (ScreenHeight) of mouse position to RobotLen
do this all the time
    get mouse position x, y
    calculate RobotLen rx, ry
    send (rx, ry) over socket

how to end program through keyboard?
'''
###############################################################
# to allow for socket communication
import socket
import sys
print(sys.version)
import time

# to acces screensize
import ctypes

# to get current mouse position
from ctypes import windll, Structure, c_ulong, byref

###############################################################
 
HOST = ''   # Symbolic name meaning all available interfaces
PORT = 30000  # Arbitrary non-privileged port

RobotXLen = 500
RobotYLen = 500

ctr = 0

user32 = ctypes.windll.user32

###Gets the screen size in Width and Height
ScreenWidth = user32.GetSystemMetrics(0)
ScreenHeight = user32.GetSystemMetrics(1)

RatioX = RobotXLen/ScreenWidth
RatioY = RobotYLen/ScreenHeight

# open a socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket created")
 
# bind socket to host and port, also catch exception.
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()
     
print('Socket bind complete')
 
# start listening to the socket
s.listen(10)
print('Socket now listening')


class POINT(Structure):
    _fields_ = [("x", c_ulong), ("y", c_ulong)]

'''
def getscreenresolution():
    print ('ScreenWidth = ' + str(ScreenWidth))
    print ('ScreenHeight = ' + str(ScreenHeight))
getscreenresolution()
'''

### gets the current mouseposition

def queryMousePosition():
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return { "x": pt.x, "y": pt.y}

### First definition of current mouseposition
pos = queryMousePosition()
posprev = queryMousePosition()

### Calculate new x and y coordinate according to ratio in x and y based on 'screenresolution' and 'RobotLen'
def CalculateRxRy():
    global rx
    global ry
    rx = pos["x"]*RatioX
    ry = pos["y"]*RatioY

### First definition and print of mouseposition and recalculated mouseposition
rx = pos["x"]
ry = pos["y"]

CalculateRxRy()

print("Rx and Ry calculated")
print(pos)
print("Rx=", rx, ", Ry=", ry)

print("here1")

conn, addr = s.accept()
print ('Connected with ' + addr[0] + ':' + str(addr[1]))

print("here2")

while 1:
    pos = queryMousePosition()
    request = conn.recv(1024)
    print(request)
    if (pos != posprev) and (request==b'1'):
        request=0
        CalculateRxRy()
        print(pos)
        print("Rx=", rx, ", Ry=", ry)
        posprev=pos
        URtarget = "("+str(rx/-1000)+", "+str(ry/-1000)+")"
        print (URtarget)
        conn.sendall(URtarget.encode())
    time.sleep(0.1)

''' Voorbeeld uit Zacobria
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.send (?set_digital_out(2,False)? + ?\n?)
data = s.recv(1024)
s.close()
print (?Received?, repr(data))
'''
 
#now keep talking with the client

#while 1:
#wait to accept a connection - blocking call
conn, addr = s.accept()
print ('Connected with ' + addr[0] + ':' + str(addr[1]))
     
data = conn.recv(1024)
reply = 'OK...' + data
#if not data: 
#    break
     
conn.sendall(reply)

# close the connection and socket after talking to the client
conn.close()
s.close()


