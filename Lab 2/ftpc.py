# Dan Shawlson
# CSE 3461, T/Th 12:45
# Lab 2

# CLI interface for FTP client

import sys
import os
import ftp_client

# Check for correct number of arguments
if (len(sys.argv) != 3):
    sys.exit('Usage: python3 ftpc.py <remote host> <remote port> <file>')

# Create FTP client
client = FTPClient(sys.argv[0], int(sys.argv[1]))

# Open file to be copied
file = open(sys.argv[2], 'rb')

# Transfer and close file
client.transfer(file)
file.close()
