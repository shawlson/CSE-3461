# Dan Shawlson
# CSE 3461, T/Th 12:45
# Lab 3

# Methods that define how communication will be handled

import socket
import sys
import os
import time

# Maximum amount of file payload to be sent at a time
chunk_size = 1000

# Define client side outbound communication handling
def CLIENT(sock, out_address, out_port, out_file, header_address, header_port):
    
    # Each UDP segment sent contains 4 bytes for remote IP address,
    # 2 bytes for remote port, and 1 byte for appropriate flag
    ip_bytes = bytes(map(int, header_address.split('.')))
    port_bytes = header_port.to_bytes(2, byteorder='big')
    header = ip_bytes + port_bytes

    # Flags represent type of segment being sent
    size_flag = int.to_bytes(1, 1, byteorder='big')
    name_flag = int.to_bytes(2, 1, byteorder='big')
    data_flag = int.to_bytes(3, 1, byteorder='big')

    # Sleep for a short amount of time after sending each segment
    sleep_time = 0.01

    # First segment - 4 bytes for size of file
    file_size = os.path.getsize(out_file.name).to_bytes(4, byteorder='big')
    seg = header + size_flag + file_size
    sock.sendto(seg, (out_address, out_port))
    time.sleep(sleep_time)

    # Second segment - 20 bytes for file name
    padding = bytearray(20)
    base_file_name = os.path.basename(out_file.name)
    file_name = bytearray(base_file_name, 'ascii') + padding[len(base_file_name):]
    seg = header + name_flag + file_name
    sock.sendto(seg, (out_address, out_port))
    time.sleep(sleep_time)

    # Rest of segments - send file data
    while True:
        chunk = bytearray(out_file.read(chunk_size))
        if len(chunk) == 0:
            break
        else:
            seg = header + data_flag + chunk
            sock.sendto(seg, (out_address, out_port))
            time.sleep(sleep_time)

    
# Define server side inbound communication handling
def SERVER(sock):

    # Flags represent type of segment being received
    FLAG_POS = 6
    size_flag = 1
    name_flag = 2
    data_flag = 3

    # Initial values
    know_size = False
    know_name = False
    file_size = None
    file_name = None
    out_file = None
    bytes_recvd = 0
    max_seg_size = 7 + chunk_size # Header + biggest possible chunk of data
    progress = '\rReceived {}B/{}B of file {}'

    while True:

        # Break once we receive full file
        if bytes_recvd == file_size:
            break

        # Listen for segment
        try:
            data = sock.recv(max_seg_size)
            # Once we receive first segment, if we don't receive any more segments for
            # 3 seconds, we assume we're done listening
            sock.settimeout(3)
        except socket.timeout:
            print('\nTimed out before full file received')
            break

        # Segment with size of file received
        if data[FLAG_POS] == size_flag:
            size_info = data[7:]
            file_size = int.from_bytes(size_info, byteorder='big')
            know_size = True
            print('Expecting file of {} bytes'.format(file_size))

        # Segment with file name received
        elif data[FLAG_POS] == name_flag:
            name_info = data[7:]
            file_name = name_info.decode('ascii').rstrip('\0')
            know_name = True
            # Create file, and directory if necessary
            os.makedirs('recv', exist_ok=True)
            out_file = open('recv/' + file_name, 'wb')
            print('Expecting file named {}'.format(file_name))

        # Segment with file data received
        elif data[FLAG_POS] == data_flag:
            if know_name and know_size:
                chunk_bytes = data[7:]
                bytes_recvd += len(data[7:])
                sys.stdout.write(progress.format(bytes_recvd, file_size, file_name))
                out_file.write(chunk_bytes)
            else:
                sock.close()
                sys.exit('Failure: data received before file name. Exiting.')

    if out_file is not None:
        out_file.close()
    print()
