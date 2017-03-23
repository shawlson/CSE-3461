# Dan Shawlson
# CSE 3461, T/Th 12:45
# Lab 4

# Define how the client will communicate with the server

import socket
import sys
import os

# Maximum amount of file payload to be sent at a time
chunk_size = 1000

# Define client side outbound communication handling
def init(dest_addr, header_addr):

    def client(sock, out_file):

        # Each UDP segment sent contains 4 bytes for remote IP address,
        # 2 bytes for remote port, 1 byte for appropriate flag, and
        # 1 byte for packet sequence number
        ip_bytes = bytes(map(int, header_addr[0].split('.')))
        port_bytes = header_addr[1].to_bytes(2, byteorder='big')
        header = ip_bytes + port_bytes

        # Flags represent type of segment being sent
        size_flag = int.to_bytes(1, 1, byteorder='big')
        name_flag = int.to_bytes(2, 1, byteorder='big')
        data_flag = int.to_bytes(3, 1, byteorder='big')

        # Alternating bits distinguish each new packet.
        current_bit = 0
        num_bits = 2

        # Create first segment - 4 bytes for size of file
        file_size = os.path.getsize(out_file.name).to_bytes(4, byteorder='big')
        packet_id = int.to_bytes((current_bit % num_bits), 1, byteorder='big')
        seg = header + size_flag + packet_id + file_size
        
        # Send/resend segment until ACK received
        send_til_ackd(sock, dest_addr, seg, current_bit)
        current_bit += 1

        # Create second segment - 20 bytes for file name
        padding = bytearray(20)
        base_file_name = os.path.basename(out_file.name)
        file_name = bytearray(base_file_name, 'ascii') + padding[len(base_file_name):]
        packet_id = int.to_bytes((current_bit % num_bits), 1, byteorder='big')
        seg = header + name_flag + packet_id + file_name

        # Send/resend segment until ACK received
        send_til_ackd(sock, dest_addr, seg, current_bit)
        current_bit += 1

        # Rest of segments - send file data
        while True:
            chunk = bytearray(out_file.read(chunk_size))
            if len(chunk) == 0:
                break
            else:
                packet_id = int.to_bytes((current_bit % num_bits), 1, byteorder='big')
                seg = header + data_flag + packet_id + chunk
                send_til_ackd(sock, dest_addr, seg, current_bit)
                current_bit += 1

    return client

def send_til_ackd(sock, addr, seg, bit):
    timeout = 0.005
    ack = False
    sock.sendto(seg, addr)
    while not ack:
        read, write, err = select.select([sock], [], [], timeout)
        if len(read) > 0:
            acked = read[0].recv(1)
            if acked == bit:
                ack = True
            else:
                sock.sendto(seg, addr)
