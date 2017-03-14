# Dan Shawlson
# CSE 3461, T/Th 12:45
# Lab 3

# FTP Server object opens and binds socket, passes it to
# protocol handler to receive transfers, then closes
# socket

import socket
import sys
import os

class FTPServer:

    def __init__(self, protocol, PORT, HOST=''):
        self._protocol = protocol
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.bind((HOST, PORT))

    # Here we simply pass the socket to its protocol handler,
    # then close it afterwards.
    def start(self):
        self._protocol(self._sock)
        self._sock.close()
