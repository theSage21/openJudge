#! /bin/bash
echo "python2.sh <codepath> <testpath>"
echo "-----------------------------------------------"
python3 /home/ghost/dev/programming/wrappers/input.py $2|python3 $1 >temp_output
echo "-----------------------------------------------"
exit
