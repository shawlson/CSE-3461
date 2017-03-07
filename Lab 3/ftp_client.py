# Dan Shawlson
# CSE 3461, T/Th 12:45
# Lab 3

# FTP Client object opens and binds socket when transfer is called,
# passes socket to protocol handler, then closes socket

import socket
import sys
import os

class FTPClient:

    def __init__(self, protocol, out_address, out_port, local_port, header_address, header_port):
        self._protocol = protocol
        self._out_address = out_address
        self._out_port = out_port
        self._local_port = local_port
        self._header_address = header_address
        self._header_port = header_port

    def transfer(self, out_file):

        # All future operations on the sock object will fail
        # once we close it, so it can't be an instance property
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', self._local_port))

        # Pass outbound address and port to protocol handler, then close it
        self._protocol(sock, self._out_address, self._out_port, out_file, self._header_address, self._header_port)
        sock.close()
        