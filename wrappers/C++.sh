#! /bin/bash
name=$RANDOM
g++ $2 -o $name  && \
$name < $1  && \
rm $name
