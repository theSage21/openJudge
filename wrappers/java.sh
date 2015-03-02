#! /bin/bash
echo "java.sh <codepath> <testpath>"
cp $1 ./source.java
javac ./source.java
python3 input.py $2|java ./source.class > temp_output
echo "comparing outputs"
cmp temp_output temp_output_file
echo "Comparison complete"
exit
