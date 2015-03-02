#! /bin/bash
echo "gcc.sh <codepath> <testpath>"
gcc $1
echo "--------------------------------------------------"
python3 /home/ghost/dev/programming/wrappers/input.py $2|./a.out >temp_output
echo "--------------------------------------------------"
echo "Comparing outputs"
cmp temp_output temp_output_file
echo "Comparison complete"
rm temp_output temp_output_file a.out
exit
