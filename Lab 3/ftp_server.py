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
        self._host = HOST
        self._port = PORT

    # Here we create the socket, pass it to its protocol handler,
    # then close it afterwards.
    def start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self._host, self._port))
        self._protocol(sock)
        sock.close()
