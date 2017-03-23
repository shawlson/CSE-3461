# Dan Shawlson
# CSE 3461, T/Th 12:45
# Lab 4

# CLI interface for FTP server

import sys
import os
import ftp_server
import server_protocol

# Check usage
if len(sys.argv) != 2:
    sys.exit('usage: ftps.py <local port> <troll port>')

# Load initial values into server protocol
dest_addr = ('', int(sys.argv[2]))
protocol = server_protocol.init(dest_addr)

# Create server object
local_port = int(sys.argv[1])
server = ftp_server.FTPServer(protocol, local_port)

# Start server
server.start()
