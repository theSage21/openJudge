OpenJudge
=========

v 0.4.0

A judge made to judge the programming competitions held over LAN.

- python3
- python2
- gcc
- g++
- java
- Perl
 
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
./setup.sh
```


`./setup.sh` does most of the work for you.


The interface is set up as a standard django server. I prefer using Nginx,Gunicorn as a 
combination. Check my [blog](http://arjoonn.blogspot.com/2015/05/django-gunicorn-and-nginx.html) for how to set that up.
`setup.sh` only sets up the code for you. You still need to deploy on your own.

To run the server you can run `./server.sh` which will set up the local Gunicorn server on port 8000.
You may then use a reverse proxy to serve it publicly.

Note that the judge will have to run on a linux like machine. I shamelessly used redirection
and I have no idea how they translate on a windows box if they do at all.

Interfaces
----------

You can use one of several interfaces available in `openjudge/interfaces` by copying one of the folders
to the directory with openjudge in it. For example:  
`$ cp -r openjudge/interfaces/bootstrap/ openjudge/templates`

Available interfaces

- bootstrap
- hackerEarth

If you come up with a new interface  

1. Name it (myinterface)
2. Create the directory inside interfaces (interfaces/myinterface)
3. Craete a pull request!
Usage during the competition
----------------------------

1. Run the interface with `./server.sh`
2. Signup users
    - Signup
    - Login
    - Register for a contest
3. Tell everyone to navigate to the webserver. It will be something like `192.168.xxx.yyy`
4. Enjoy the fruits of watching a hundred people program.

Gotchas
-------
Some features are not available since they are particularly difficult to implement as
plug and play services. If you want you can implement them yourself.

- No sandboxing.
