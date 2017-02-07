# Dan Shawlson
# CSE 3461, T/Th 12:45
# Lab 2

# CLI interface for FTP server

import sys
import os
import ftp_server

# Check usage and get port number
if len(sys.argv) != 2:
    sys.exit('usage: ftps.py <port number>')

port = int(sys.argv[-1])

# Define connection handling
def handler(conn):

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
    progress = '\rReceived {}B/{}B of file {}'\
              .format(bytes_received, file_size, file_name)
    sys.stdout.write(progress)
    
    while True:
        data = conn.recv(512)
        if not data:
            break
        else:
            bytes_received += len(data)
            progress = '\rReceived {}B/{}B of file {}'\
                      .format(bytes_received, file_size, file_name)
            sys.stdout.write(progress)
            out_file.write(data)

    # Close connection and file
    print('\nDone receiving {}'.format(file_name))
    conn.close()
    out_file.close()

# Start server
server = ftp_server.FTPServer(port)
server.listen(handler)
