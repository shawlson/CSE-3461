# Dan Shawlson
# CSE 3461, T/Th 12:45
# Lab 2

# FTP Server object that continualy listens on
# the specified port.

import socket
import sys
import os

class FTPServer:

    def __init__(self, PORT, HOST=''):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind((HOST, PORT))

    # Here we only listen for a connection. The handler function
    # passed in handles any busines logic
    def listen(self, handler):
        try:
            while True:
                self._socket.listen(1)
                conn, address = self._socket.accept()
                print('Received connection from {}'.format(address))
                handler(conn)
        except KeyboardInterrupt:
            self._socket.close()
            sys.exit()
