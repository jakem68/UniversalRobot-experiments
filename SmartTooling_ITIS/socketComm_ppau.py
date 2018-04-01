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
import socket, sys, queue, threading
from list import *

print(sys.version)


###############################################################


def main():
    HOST = ''  # Symbolic name meaning all available interfaces
    PORT = 30000  # Arbitrary non-privileged port
    q = queue.Queue()
    thread_sock = threading.Thread(target=create_socket_connection, args=(HOST, PORT, q))
    thread_sock.start()

    # conn = q.get()

    while 1:
        leaks = List('leaks')
        conn = q.get()
        print(conn)
        print("attaching to new connection")
        leak_btn_state = False # checks whether a state was sent before a pose is sent
        leak_flag_value = 0
        while q.empty():
            msg_in = conn.recv(1024)
            msg_in_str = msg_in.decode()
            if msg_in_str != '':
                print(msg_in_str)
                msg = evaluate_msg(msg_in_str)  # returns a 'type' and 'value' of the message
                if msg['type'] == 'pose':
                    if leak_btn_state == True:

#                        hier zit het probleem: msg['value'] is een lijst van 6 strings en hier voeg ik een haakje van voor en van achter met een zevende string aan toe --> wss is beter gewoon append zevende item aan msg['value']
                        msg['value'] = "("+msg['value']+","+str(leak_flag_value)+")"
                        print(msg['value'])
                        print(type(msg['value']))
                        leaks.store_item(msg['value'])
                        leak_btn_state = False
                    else:
                        print('Pose received but no corresponding state of the pose received. Pose disregarded')
                elif msg['type'] == 'leak_flag':
                    if msg['value'] == 'leak':
                        leak_flag_value = 1
                    else: leak_flag_value = 0
                    leak_btn_state = True
                elif msg['type'] == 'request':
                    if msg['value'] == "request_pose":
                        leaks.send_item(conn)
                        leak_btn_state = False
                    elif msg['value'] == "request_leaks":
                        leaks.send_nr_leaks(conn)
                        leak_btn_state = False
                else:
                    print("message type of message: {0} was not recognized".format(msg_in))
        conn.close()

    # close the connection and socket after talking to the client
    s.close()


def create_socket_connection(host, port, q):
    # open a socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket created")
    # bind socket to host and port, also catch exception.
    try:
        s.bind((host, port))
    except socket.error as msg:
        print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
        sys.exit()
    print('Socket bind complete')
    # start listening to the socket

    while True:
        s.listen(2)
        print('Socket now listening')
        # server keeps listening, program continues only when connection is made
        conn, addr = s.accept()
        print('Connected with ' + addr[0] + ':' + str(addr[1]))

        # return conn
        q.put(conn)


# evaluation of list momentarily purely on number of items in the list:
#   6 items = pose
#   1 item = request or maybe something else later
def evaluate_msg(str_in):
    str_list = str_in.split(",")
    #    print(str_list)
    #    print(len(str_list))
    if len(str_list) == 6:
        pose = convert_str_list_to_pose(str_list)
        msg_type = "pose"
        msg = {"type": msg_type, "value": pose}
        #        print(msg)
        return msg
    if len(str_list) == 1:
        if str_list[0]=="request_pose":
#            msg_type = "request"
            msg = {"type": 'request', "value": str_list[0]}
        elif str_list[0]=="request_leaks":
            msg = {"type": 'request', "value": str_list[0]}
        elif str_list[0]=="leak":
            msg = {"type": 'leak_flag', "value": str_list[0]}
        elif str_list[0]=="no_leak":
            msg = {"type": 'leak_flag', "value": str_list[0]}
        else:
            print('message not understood.')
        return msg

    return True


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
    # print(float_list[2])
    # float_list[2] = float_list[2] - 0.2
    # print(float_list[2])

    # convert recalculated floats back to list of strings
    for i in range(len(float_list)):
        str_list[i] = repr(float_list[i])

    # make one string out of list of strings with the p[ and ] for UR
    pose_str = ",".join(str_list)
#    pose_str = "p[" + pose_str + "]"
    # print ("pose_str is: {}".format(pose_str))

    return pose_str


if __name__ == "__main__":
    main()
