# Dan Shawlson
# CSE 3461, T/Th 12:45
# Lab 4

# CLI interface for FTP client

import sys
import ftp_client
import protocol.client

# Check usage
if len(sys.argv) != 5:
    sys.exit('Usage: python3 ftpc.py <IP-address-of-gamma> <remote-port-on-gamma> <troll–port-on-beta> <local-file-to-transfer>')

# Load initial values into client protocol
dest_addr = ('', int(sys.argv[3]))
header_addr = (sys.argv[1], int(sys.argv[2]))
protocol = protocol.client.init(dest_addr, header_addr)

# Creat client object. Local port is arbitrary
client = ftp_client.FTPClient(5195, protocol)

# Open file to be copied
out_file = open(sys.argv[4], 'rb')

# Transfer and close file
client.transfer(out_file)
out_file.close()
