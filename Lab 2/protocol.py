# Dan Shawlson
# CSE 3461, T/Th 12:45
# Lab 2

import socket
import sys
import os

# Methods that define how communication will be handled

# Define client side outbound communication handling
def CLIENT(conn, out_file):

    chunk_size = 512

    # Start sending protocol information
    # First 4 bytes - size of file in bytes, big endian
    file_size = os.path.getsize(out_file.name)
    conn.send(file_size.to_bytes(4, byteorder='big'))

    # Next 20 bytes - name of file, assumed <= 20
    padding = bytearray(20)
    base_file_name = os.path.basename(out_file.name)
    conn.send(bytearray(base_file_name, 'ascii') + padding[len(base_file_name):])

    # Read and send until end of file
    while True:
        chunk = bytearray(out_file.read(chunk_size))
        if len(chunk) == 0:
            break
        else:
            conn.send(chunk)


# Define server side inbound communication handling
def SERVER(conn):

    # First 4 bytes indicate file size
    data = conn.recv(4)
    file_size = int.from_bytes(data, byteorder='big')

    # Next 20 bytes indicate file name. Convert them to string
    # and strip any trailing null characters
    data = conn.recv(20)
    file_name = data.decode('ascii').rstrip('\0')

    # Create file, and directory if necessary
    os.makedirs('recv', exist_ok=True)
    out_file = open('recv/' + file_name, 'wb')

    # Receive the transfer in chunks and write them to file
    bytes_received = 0
    progress = '\rReceived {}B/{}B of file {}'
    sys.stdout.write(progress.format(bytes_received, file_size, file_name))
    
    while True:
        data = conn.recv(512)
        if not data:
            break
        else:
            bytes_received += len(data)
            sys.stdout.write(progress.format(bytes_received, file_size, file_name))
            out_file.write(data)

    # Close connection and file
    print('\nDone receiving {}'.format(file_name))
    out_file.close()
