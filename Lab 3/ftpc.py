# Dan Shawlson
# CSE 3461, T/Th 12:45
# Lab 3

# CLI interface for FTP client

import sys
import os
import ftp_client
import protocol

# Check for correct number of arguments
if len(sys.argv) != 5:
    sys.exit('Usage: python3 ftpc.py <IP-address-of-gamma> <remote-port-on-gamma> <troll–port-on-beta> <local-file-to-transfer>')

# Create FTP client
client = ftp_client.FTPClient(protocol=protocol.CLIENT, out_address='', out_port=int(sys.argv[3]), local_port=5195,
                              header_address=sys.argv[1], header_port=int(sys.argv[2]))

# Open file to be copied
out_file = open(sys.argv[4], 'rb')

# Transfer and close file
client.transfer(out_file)
out_file.close()
