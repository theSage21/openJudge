#! /bin/bash
echo "python2.sh <input_path> <source_code>"
echo "-----------------------------------------------"
python3 ./input.py $1|python2 $2 >temp_output
echo "-----------------------------------------------"
exit
