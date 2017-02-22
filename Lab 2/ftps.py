# Dan Shawlson
# CSE 3461, T/Th 12:45
# Lab 2

# CLI interface for FTP server

import sys
import os
import ftp_server
import protocol

# Check usage and get port number
if len(sys.argv) != 2:
    sys.exit('usage: ftps.py <port number>')

port = int(sys.argv[-1])

# Start server
server = ftp_server.FTPServer(port)
server.listen(protocol.SERVER)
