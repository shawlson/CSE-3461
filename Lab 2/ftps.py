# Dan Shawlson
# CSE 3461, T/Th 12:45
# Lab 2

import socket

HOST = ''
PORT = 43210

_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
_socket.bind((HOST, PORT))
_socket.listen(1)
conn, addr = _socket.accept()
print('Received connection')

data = conn.recv(512)
# First 4 bytes indicate file size
file_size = int.from_bytes(data[:4], byteorder='big')
print(file_size)
# Next 20 bytes indicate file name. Convert them to string
# and strip any trailing null characters
file_name = data[4:24].decode('ascii').rstrip('\0')
print(file_name)

# Create file and begin writing data to it
out_file = open(file_name, 'wb')
out_file.write(data[24:])

# Receive the rest of the data in chunks and write them to file
while True:
    data = conn.recv(512)
    if not data:
        break
    else:
        out_file.write(data)

# Close connection and file
conn.close()
out_file.close()
