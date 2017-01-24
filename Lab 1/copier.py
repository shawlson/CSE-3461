# Dan Shawlson
# CSE 3461, T/Th 12:45
# Lab 1

# Code to handle copying of bytes from input file to output file.
# Trivial at this point, but I assume since the labs build off each
# other this will become the logic to do file transfers over a network,
# or something like that

import sys
import os

def copy(in_file, out_file):
    
    chunk_size = 512

    # Read 512 bytes from in_file and write them to out_file, until we
    # reach the end of in_file
    while True:
        data_buffer = in_file.read(chunk_size)
        if len(data_buffer) == 0:
            break
        else:
            out_file.write(data_buffer)
