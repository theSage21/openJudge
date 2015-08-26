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

```
cd ~
mkdir judge
cd judge
virtualenv -p python3 env
source env/bin/activate
pip install openjudge
```

The interface for the Judge does not ship with the judge.

The interface I use is [judge-interface](https://github.com/theSage21/judge-interface).

In order to use that one can do the following.

```
cd ~
git clone https://github.com/theSage21/judge-interface.git
cd judge-interface
./setup.sh
```

1. `./setup.sh` does most of the work for you.
2. Set the SLAVE_ADDRESSES in settings.py by default it is set to 127.0.0.1:9000

The interface is set up as a standard django server. I prefer using Nginx,Gunicorn as a 
combination. Check my [blog](http://arjoonn.blogspot.com/2015/05/django-gunicorn-and-nginx.html) for how to set that up.

Note that the slave will have to run on a linux like machine. I shamelessly used redirection
and I have no idea how they translate on a windows box if they do at all.

Usage during the competition
----------------------------

1. Register users with `python add_user.py` using a python shell at the registration desk.
   the file can be found in `judge-interface/webserver/`
2. Run the interface with `./runserver.sh`
3. Run the judge with `python -c 'from openjudge.slave import Slave;Slave().run()'`
3. Tell everyone to navigate to the webserver. It will be something like `192.168.1.45`
4. Enjoy the fruits of watching a hundred people program.
