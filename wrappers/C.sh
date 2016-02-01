#! /bin/bash
name=$RANDOM
gcc $2 -o ./$name && \
./$name < $1 && \
rm ./$name
