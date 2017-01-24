#!/bin/bash
SAMPLES=Samples/*
for f in $SAMPLES; do
  no_erase=1
  python3 ../copy.py $f
  filename=$(basename $f)
  if [ -d "recv/" ]; then
    if [ -f "recv/$filename" ]; then
      if diff $f recv/$filename; then
        echo "$f copied successfully"
      else
        no_erase=0
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

if [ $no_erase ]; then
rm -rf recv
fi
