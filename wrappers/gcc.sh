#! /bin/bash
echo "gcc.sh <input> <code> <out_file_name>"
gcc $2
echo "--------------------------------------------------"
./a.out < $1 > $3
