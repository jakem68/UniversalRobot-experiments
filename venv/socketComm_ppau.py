#!/usr/bin/env python

__author__ = 'Jan Kempeneers'


'''
do this once
    create server
    open socket
    read socket
    evaluate string
'''
###############################################################
# to allow for socket communication
import socket, sys
from list import *

print(sys.version)


###############################################################


def main():
    conn = create_socket_connection()

    leaks = List('leaks')
    while 1:
        msg_in = conn.recv(1024)
        msg_in_str = msg_in.decode()
        if msg_in_str != '':
            print(msg_in_str)
            msg = evaluate_msg(msg_in_str)  # returns a 'type' and 'value' of the message
            if msg['type'] == 'pose':
                print('here', msg['value'])
                leaks.store_item(msg['value'])
            elif msg['type'] == 'request':
                leaks.send_item(conn)
            else:
                print("message type of message: {} was not recognized", format(msg_in))

            # msg komt binnen als : b'p(float1, float2, float3, float4, float5, float6)' request komt binnen als b'1'
            # als er niets is komt b'' try the following: print (type(msg_in)) print (repr(msg_in)) print (
            # msg_in.decode()) sending in byte format to UR as follows: mystring.encode('utf-8')

        # if (pos != posprev) and (request == b'1'):
        #     request = 0
        #     CalculateRxRy()
        #     print(pos)
        #     print("Rx=", rx, ", Ry=", ry)
        #     posprev = pos
        #     URtarget = "(" + str(rx / -1000) + ", " + str(ry / -1000) + ")"
        #     print(URtarget)
        #     conn.sendall(URtarget.encode())
        # time.sleep(0.1)

    # close the connection and socket after talking to the client
    conn.close()
    s.close()


def create_socket_connection():
    HOST = ''  # Symbolic name meaning all available interfaces
    PORT = 30000  # Arbitrary non-privileged port
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
    # server keeps listening, program continues only when connection is made
    conn, addr = s.accept()
    print('Connected with ' + addr[0] + ':' + str(addr[1]))
    return conn


# turns received txt msg into six floats to allow for calculations and then reformats the result to represent a clean
#  pose string format for UR
def convert_str_list_to_pose(str_list):
    str_list[0] = str_list[0][2:]
    str_list[5] = str_list[5][:-1]

    float_list = []
    # convert list of strings to list of floats
    for str in str_list:
        float_list.append(float(str))
    # if necessary return float_list here

    # possibly do some calculations on floats in float_list here

    # convert recalculated floats back to list of strings
    for i in range(len(float_list)):
        str_list[i] = repr(float_list[i])
        print(str_list[i])

    # make one string out of list of strings with the p[ and ] for UR
    pose_str = ",".join(str_list)
    pose_str = "p[" + pose_str + "]"
    # print ("pose_str is: {}".format(pose_str))

    return pose_str


# evaluation of list momentarily purely on number of items in the list:
#   6 items = pose
#   1 item = request or maybe something else later
def evaluate_msg(str_in):
    str_list = str_in.split(",")
    print(str_list)
    print(len(str_list))
    if len(str_list) == 6:
        pose = convert_str_list_to_pose(str_list)
        msg_type = "pose"
        msg = {"type": msg_type, "value": pose}
        print(msg)
        return msg
    if len(str_list) == 1:
        msg_type = "request"
        msg = {"type": msg_type, "value": 'request'}
        return msg

    return True


if __name__ == "__main__":
    main()
