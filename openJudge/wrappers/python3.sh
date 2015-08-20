#! /bin/bash
echo "python3.sh <input> <code> <out_file_name>"
echo "-----------------------------------------------"
python3 $2 < $1 > $3
