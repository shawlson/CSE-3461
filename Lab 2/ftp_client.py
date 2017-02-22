# Dan Shawlson
# CSE 3461, T/Th 12:45
# Lab 2

# FTP Client object establishes connection to server
# and includes method to send file to server

import socket
import sys
import os

class FTPClient:

    @property
    def address(self):
        return self._address

    @property
    def port(self):
        return self._port

    def __init__(self, address, port):
        self._address = address
        self._port = port

    def transfer(self, out_file, handler):

        # All future operations on the _socket object will fail
        # once we close it, so it can't be an instance property
        _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to remote socket, pass it to handler, then close it
        _socket.connect((self._address, self._port))
        handler(_socket, out_file)
        _socket.close()
        