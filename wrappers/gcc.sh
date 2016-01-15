#! /bin/bash
name=$RANDOM
gcc $2 -o /tmp/$name
/tmp/$name < $1
rm /tmp/$name
