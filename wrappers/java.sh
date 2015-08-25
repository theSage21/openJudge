#! /bin/bash
source_file=$2
class_file=${source_file%.java}.class
javac $source_file>>temp_output
cp $class_file ./
output_file=${class_file##*/}
output_call_name=${output_file%.class}
java $output_call_name < $1
