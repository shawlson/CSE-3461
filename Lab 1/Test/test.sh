#!/bin/bash

# Sample files to be copied stored in Samples directory
SAMPLES=Samples/*

for f in $SAMPLES; do

  # We erase all copied files and recv subdirectory on success
  erase=1

  # Run program on sample
  python3 ../copy.py $f

  filename=$(basename $f)
  # If recv subdirectory not created, exit
  if [ -d "recv/" ]; then
    # If copy of file with correct name not created, exit
    if [ -f "recv/$filename" ]; then
      # Alert whether file was copied correctly.
      # If files differ, don't erase the copy
      if diff $f recv/$filename; then
        echo "$f copied successfully"
      else
        erase=0
        echo "$f differs from recv/$filename"
      fi
    else
      echo "Output file recv/$filename not created"
      exit
    fi
  else
    echo "recv directory not created"
    exit
  fi
done

if [ $erase ]; then
  rm -rf recv
fi
