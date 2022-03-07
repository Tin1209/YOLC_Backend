from socket import * 
from select import * 
import sys
from time import ctime


def open_door(isOpen):
    HOST = 'heean6620.iptime.org'
    PORT = 9999
    BUFSIZE = 1024
    ADDR = (HOST,PORT)

    clientSocket = socket(AF_INET, SOCK_STREAM)

    try:
       clientSocket.connect(ADDR)
    except Exception as e:
       print('%s:%s' %ADDR)
       sys.exit()
    print('connect is success')


    sendData = str(isOpen)
    clientSocket.send(sendData.encode())
