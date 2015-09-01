#! /bin/bash
source env/bin/activate
python -c 'from openjudge import slave, __version__, config;
print(__version__);
s=slave.Slave();s.run()'
