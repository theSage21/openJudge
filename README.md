OpenJudge
=========

A judge made to judge the programming competitions held over LAN.

- python3
- python2
- gcc
- g++
- java
 
Supported out of the box.

Why?
----

- Judging programs by hand quickly becomes an experience best forgotten
- Roll-my-own

Setup
-----

```
cd ~
git clone --depth 1  https://github.com/theSage21/openjudge
virtualenv -p python3 env
source env/bin/activate
./setup.sh
```


`./setup.sh` does most of the work for you.


The interface is set up as a standard django server. I prefer using Nginx,Gunicorn as a 
combination. Check my [blog](http://arjoonn.blogspot.com/2015/05/django-gunicorn-and-nginx.html) for how to set that up.
`setup.sh` only sets up the code for you. You still need to deploy on your own.

Note that the judge will have to run on a linux like machine. I shamelessly used redirection
and I have no idea how they translate on a windows box if they do at all. Besides that, 
the interface can run on another machine and the judge on another.

Usage during the competition
----------------------------

1. Run the interface with `./server.sh`
2. Signup users
    - Signup
    - Login
    - Register for a contest
3. Tell everyone to navigate to the webserver. It will be something like `192.168.1.45`
4. Enjoy the fruits of watching a hundred people program.

Gotchas
-------
Some features are not available. If you want you can implement them yourself.

- No sandboxing.
