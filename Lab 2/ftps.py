# Dan Shawlson
# CSE 3461, T/Th 12:45
# Lab 2

import socket
import os
import sys

# Check usage and get port number
if len(sys.argv) != 2:
    sys.exit('usage: ftps.py <port number>')

PORT = int(sys.argv[-1])

# Listen on port specified until connection received
HOST = ''
_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
_socket.bind((HOST, PORT))
_socket.listen(1)
conn, addr = _socket.accept()
print('Received connection')

data = conn.recv(512)
# First 4 bytes indicate file size
file_size = int.from_bytes(data[:4], byteorder='big')
# Next 20 bytes indicate file name. Convert them to string
# and strip any trailing null characters
file_name = data[4:24].decode('ascii').rstrip('\0')


# Create file, and directory if necessary, and begin writing data to it
os.makedirs('recv', exist_ok=True)
out_file = open('recv/' + file_name, 'wb')
out_file.write(data[24:])
bytes_received = len(data[24:])

# Receive the rest of the data in chunks and write them to file
while True:
    data = conn.recv(512)
    if not data:
        break
    else:
        bytes_received += len(data)
        out_file.write(data)

# Check for mistakes in transmission
if bytes_received != file_size:
    print('ERROR')
    print('{file_size} bytes expected, but {bytes_received} bytes received'\
          .format(file_size, bytes_received))
          
# Close connection and file
conn.close()
out_file.close()
