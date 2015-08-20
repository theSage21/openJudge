#! /bin/bash
echo "g++.sh <input> <code> <out_file_name>"
g++ $2
echo "--------------------------------------------------"
./a.out < $1 > $3
