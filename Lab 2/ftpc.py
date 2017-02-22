# Dan Shawlson
# CSE 3461, T/Th 12:45
# Lab 2

# CLI interface for FTP client

import sys
import os
import ftp_client
import protocol

# Check for correct number of arguments
if len(sys.argv) != 4:
    sys.exit('Usage: python3 ftpc.py <remote host> <remote port> <file>')

# Create FTP client
client = ftp_client.FTPClient(sys.argv[1], int(sys.argv[2]))

# Open file to be copied
out_file = open(sys.argv[3], 'rb')

# Transfer and close file
client.transfer(out_file, protocol.CLIENT)
out_file.close()
