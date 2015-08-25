#! /bin/bash
source env/bin/activate
python -c 'from openjudge.slave import Slave;s=Slave();s.run()'
