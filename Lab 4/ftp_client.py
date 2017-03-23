# Dan Shawlson
# CSE 3461, T/Th 12:45
# Lab 4

# FTP Client object opens and binds socket when transfer is called,
# passes socket to protocol handler, then closes socket

import socket
import sys
import os

class FTPClient:

    def __init__(self, local_port, protocol):
        self._local_port = local_port
        self._protocol = protocol

    def transfer(self, out_file):

        # All future operations on the sock object will fail
        # once we close it, so it can't be an instance property
        #
        # Normally we wouldn't bind a client UDP socket, but troll
        # requires it.
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', self._local_port))

        # Pass outbound address and port to protocol handler, then close it
        self._protocol(sock, out_file)
        sock.close()
        