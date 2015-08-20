OpenJudge
=========
[![Build Status](https://travis-ci.org/theSage21/openJudge.svg)](https://travis-ci.org/theSage21/openJudge)

A judge I made to judge the simple programming competitions in college.
A django based web server to provide the interface and a python3 based
checking server.


Supports python3,python2,java,c++,c. for the attempt languages.
Checks the code via simple shell script wrappers and pipes and output comparison.

Setup
-----

The webserver and the checkserver may be set up on different machines. In fact it is 
recommended to do so. Allowing people to run arbitrary code on the machine which runs
your webserver is generally a bad idea.

1. `./setup.sh` does most of the work for you.
2. Set the SLAVE_ADDRESSES in settings.py by default it is set to 127.0.0.1:9000
3. Run the webserver. I usually set up using gunicorn and nginx. `./runserver.sh`
4. Run the check server by executing the slave.py file `./runslave.sh`

The webserver is set up as a standard django server. I prefer using Nginx,Gunicorn as a 
combination. Check my [blog](http://arjoonn.blogspot.com/2015/05/django-gunicorn-and-nginx.html) for how to set that up.

Note that the slave will have to run on a linux like machine. I shamelessly used redirection
and I have no idea how they translate on a windows box if they do at all.

Usage during the competition
----------------------------

1. Register users with `python add_user.py` using a python shell at the registration desk.
   the file can be found in `./openJudge/webserver/`
2. Run the webserver. Run the check server. Use above instructions
3. Tell everyone to navigate to the webserver. It will be something like `192.168.1.45`
4. Enjoy the fruits of wwatching a hundred people program.

I recommend a virtualenv with all the requirements satisfied.
```
virtualenv -p python3 env
source env/bin/activate
pip install -r requirements-dev.txt
```

Known Pitfalls
--------------

- There are no timeouts. An infinite loop will keep the checkserver busy forever.
