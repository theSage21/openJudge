OpenJudge
=========
[![Build Status](https://travis-ci.org/theSage21/openJudge.svg)](https://travis-ci.org/theSage21/openJudge)
[![Coverage Status](https://coveralls.io/repos/theSage21/openJudge/badge.svg?branch=master&service=github)](https://coveralls.io/github/theSage21/openJudge?branch=master)

A judge I made to judge the programming competitions in college.
It is a checking server and requires a web interface to function.

Currently the languages supported are:

- Python2
- Python3
- Gcc
- G++

Others may be added by adding a shell script in the `wrappers` folder.

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
4. Enjoy the fruits of watching a hundred people program.

I recommend a virtualenv with all the requirements satisfied.
```
virtualenv -p python3 env
source env/bin/activate
pip install -r requirements-dev.txt
```

This is not needed if you are running `./setup.sh`. 
