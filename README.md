OpenJudge
=========
[![Build Status](https://travis-ci.org/theSage21/openJudge.svg)](https://travis-ci.org/theSage21/openJudge)
[![Coverage Status](https://coveralls.io/repos/theSage21/openJudge/badge.svg?branch=master&service=github)](https://coveralls.io/github/theSage21/openJudge?branch=master)

A judge made to judge the programming competitions held over LAN.
It requires a web based interface to function.

Language support is unlimited, as long as you can write a shell script for it.
The interface I use is [judge-interface](https://github.com/theSage21/judge-interface).
The interface ships with

- python3
- python2
- gcc
- g++
- java

Why?
----

- Judging programs by hand quickly becomes an experience best forgotten
- Roll-my-own

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

In order to setup the interface one can do the following.

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
`setup.sh` does this for you.

Note that the judge will have to run on a linux like machine. I shamelessly used redirection
and I have no idea how they translate on a windows box if they do at all. Besides that, 
the interface can run on another machine and the judge on another.

Usage during the competition
----------------------------

1. Run the interface with `./runserver.sh`
2. Register users:
    - Register users with `python add_user.py` using a python shell at the registration desk.
      the file can be found in `judge-interface/webserver/`
    - This can also be done via the Django Admin
3. Run the judge with `openjudge`
3. Tell everyone to navigate to the webserver. It will be something like `192.168.1.45`
4. Enjoy the fruits of watching a hundred people program.

Command line options
--------------------

All options are available via command line.

| Option                                                 | Description
|--------------------------------------------------------|---------------------------------------------------
| `-v`, `--version`                                      | Show version info and exit
| `-h`, `--help`                                         | Show this help message and exit
| `-ll`, `--log-level`                                   | Logging level. Integer value accepted
| `-t`, `--timeout`                                      | The time in seconds to wait before declaring code to be timed out.
|`-d`, `--check-data-folder`                             | Path to the folder which must be used for data storage
| `-w`, `--web-server`                                   | Address of webserver. example 192.168.1.15:80
| `-u`, `--detail-url`                                   | URL where details of question and languages may be found
| `-b`, `--bind`                                         | Address where the slave must listen. example ('127.0.0.1', 9000)
| `-j`, `--job-list-prefix`                              | The prefix string used to store job list files
| `-p`, `--protocol`                                     | The protocol used by the webserver. example https://
| `-l`, `--log-file`                                     | The name of the log file to use for logging purposes


Invoke via `openjudge --help`

Gotchas
-------
Some features are not available. If you want you can implement them yourself.

- No sandboxing.
