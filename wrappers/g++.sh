#! /bin/bash
echo "g++.sh <codepath> <testpath>"
g++ $1
echo "--------------------------------------------------"
python3 /home/ghost/dev/programming/wrappers/input.py $2|./a.out >temp_output
echo "--------------------------------------------------"
exit
