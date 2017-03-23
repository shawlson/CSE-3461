# Dan Shawlson
# CSE 3461, T/Th 12:45
# Lab 4

# Define how the server will communicate with the client

import socket
import sys
import os
import time

# Maximum amount of file payload to be sent at a time
chunk_size = 1000

# Define server side inbound communication handling
def init(dest_addr):

    def server(sock):

        # Protocol constants
        FLAG_POS = 6
        SEQ_POS = 7
        PAYLOAD_POS = SEQ_POS + 1
        SIZE_FLAG = 1
        NAME_FLAG = 2
        DATA_FLAG = 3

        # Initial values
        know_size = False
        know_name = False
        file_size = None
        file_name = None
        out_file = None
        bytes_recvd = 0
        max_seg_size = 8 + chunk_size # Header + biggest possible chunk of data
        progress = '\rReceived {}B/{}B of file {}'

        while True:

            # Break once we receive full file
            if bytes_recvd == file_size:
                break

            # Listen for segment
            try:
                data = sock.recv(max_seg_size)
                send_ack(sock, dest_addr, data[SEQ_POS])
                # Once we receive first segment, if we don't receive any more segments for
                # 3 seconds, we assume we're done listening
                sock.settimeout(3)
            except socket.timeout:
                print('\nTimed out before full file received')
                break

            # Segment with size of file received
            if data[FLAG_POS] == SIZE_FLAG:
                size_info = data[PAYLOAD_POS:]
                file_size = int.from_bytes(size_info, byteorder='big')
                know_size = True
                print('Expecting file of {} bytes'.format(file_size))

            # Segment with file name received
            elif data[FLAG_POS] == NAME_FLAG:
                name_info = data[PAYLOAD_POS:]
                file_name = name_info.decode('ascii').rstrip('\0')
                know_name = True
                # Create file, and directory if necessary
                os.makedirs('recv', exist_ok=True)
                out_file = open('recv/' + file_name, 'wb')
                print('Expecting file named {}'.format(file_name))

            # Segment with file data received
            elif data[FLAG_POS] == DATA_FLAG:
                if know_name and know_size:
                    chunk_bytes = data[PAYLOAD_POS:]
                    bytes_recvd += len(data[PAYLOAD_POS:])
                    sys.stdout.write(progress.format(bytes_recvd, file_size, file_name))
                    out_file.write(chunk_bytes)
                else:
                    sock.close()
                    sys.exit('Failure: data received before file name. Exiting.')

        if out_file is not None:
            out_file.close()
        print()

    return server

def send_ack(sock, addr, bit):
    ack = int.to_bytes(bit, 1, byteorder='big')
    sock.sendto(ack, addr)
