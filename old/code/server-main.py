#!/usr/bin/python


import thread
import time
import socket
import config

from comm.websocket import WebsocketServer
from comm.tcpsocket import TcpServer

import comm.communication
from comm.communication import Communication
from comm.serial_com_mock import SerialComMock

import sys

if __name__ == "__main__":
    
    web_socket_server = None

    web_socket_server = WebsocketServer()
    thread.start_new_thread(web_socket_server.start, (config.websocket_port, ))
        
    while True:
        time.sleep(1)

