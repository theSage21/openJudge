#! /bin/bash
echo "java.sh <codepath> <testpath>"
source_file=$1
class_file=${source_file%.java}.class
echo "--------------------------------------------------"
javac $source_file>>temp_output
cp $class_file ./
output_file=${class_file##*/}
output_call_name=${output_file%.class}
echo $output_file
python3 /home/ghost/dev/programming/wrappers/input.py $2|java $output_call_name>>temp_output
echo "--------------------------------------------------"
exit
