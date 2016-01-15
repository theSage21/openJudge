#! /bin/bash
name=$RANDOM
g++ $2 -o /tmp/$name
/tmp/$name < $1
rm /tmp/$name
