# Dan Shawlson
# CSE 3461, T/Th 12:45
# Lab 4

# When start is called, FTP Server object opens and binds socket, 
# passes it to protocol handler to receive one transfer, then closes
# socket

import socket
import sys
import os

class FTPServer:

    def __init__(self, local_port, protocol):
        self._protocol = protocol
        self._local_port = local_port

    def start(self):
        # All future operations on the sock object will fail
        # once we close it, so it can't be an instance property
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', self._local_port))
        self._protocol(sock)
        sock.close()
