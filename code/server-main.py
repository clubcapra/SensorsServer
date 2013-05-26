#!/usr/bin/python


import thread
import time

import config

from comm.websocket import WebsocketServer
from comm.tcpsocket import TcpServer

import comm.communication
from comm.communication import Communication
from comm.serial_com_mock import SerialComMock

import sys

if __name__ == "__main__":
    
    # The communication interface to the sensors is defined globally
    if config.simulation is True:
        comm.communication.instance = Communication(SerialComMock()) # a mocked serial implementation
    else:
        comm.communication.instance = Communication() # real serial
        
    comm.communication.instance.start()

    if config.use_websockets is True:
        thread.start_new_thread(WebsocketServer, (config.websocket_port, ))
        
    if config.use_tcp_server is True:
        tcpServer = TcpServer(config.tcp_port)
        tcpServer.start()
        
    while True:
        time.sleep(1)


