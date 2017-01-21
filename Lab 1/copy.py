# Dan Shawlson
# CSE 3461, T/Th 12:45
# Lab 1

# Reads input file from command line, creates and opens output file
# and directory, and initiates the copy from input to output

import sys
import os
import copier

# Check for correct number of arguments
if (len(sys.argv) != 2):
    sys.exit('Usage: python3 copy.py <filename>')

# Open file to be copied
in_file = open(sys.argv[-1], 'rb')

# Create recv directory, if necessary
os.makedirs('recv', exist_ok=True)

# (Erase and) Create output file in new directory
filename = os.path.basename(sys.argv[-1])
out_file = open('recv/' + filename, 'wb')

# Copy input file to output file
copier.copy(in_file, out_file)

# Close files
in_file.close()
out_file.close()