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

    def transfer(file, chunk_size=512):

        # All future operations on the _socket object will fail
        # once we close it, so it can't be an instance property
        _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to remote socket
        _socket.connect((self._address, self._port))

        # Set up protocol header
        #   First 4 bytes - size of file in bytes, big endian
        #   Next 20 bytes - name of file, assumed <= 20
        chunk = bytearray()
        file_size = os.path.getsize(file)
        chunk += bytearray(file_size.to_bytes(4, 'big'))

        padding = bytearray(20)
        chunk += bytearray(file.name, 'ascii') + padding[len(file.name):]

        if len(chunk != 24):
            print('ERROR')
            print(chunk)

        # Start reading from file and sending chunks to server
        chunk += file.read(chunk_size - 24)  # 24 bytes for protocol
        _socket.send(chunk)

        # Read and send until end of file
        while True:
            chunk = bytearray(file.read(chunk_size))
            if len(chunk) == 0:
                break
            else:
                _socket.send(chunk)

        # Finished sending, shutdown and close socket
        _socket.shutdown()
        _socket.close()
        