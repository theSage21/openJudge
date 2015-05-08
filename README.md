OpenJudge
=========

A judge I made to judge the simple programming competitions in college.
A django based web server to provide the interface and a python3 based
checking server.


Supports python3,python2,java,c++,c. for the attempt languages.
Checks the code via simple shell script wrappers and pipes and output comparison.

Setup
-----

The webserver and the cehckserver may be set up on different machines. In fact it is 
recommended to do so. Allowing people to run arbitrary code on the machine which runs
your webserver is generally a bad idea.


1. Set the CHECK_SERVER_ADDRESS in settings.py by default it is set to 127.0.0.1:9000
2. Run the webserver. I usually set up using gunicorn and nginx.
3. Run the check server by executing the slave.py file

The webserver is set up as a standard django server. I prefer using Nginx,Gunicorn as a 
combination. Check my [blog](http://arjoonn.blogspot.com/2015/05/django-gunicorn-and-nginx.html) for how to set that up.

Note that the slave.py file will have to run on a linux like machine. I shamelessly uses pipes
and I have no idea how they translate on a windows box.

Usage during the competition
----------------------------

1. Register users with question.models.nplayer() using a python shell at the registration desk
2. Run the webserver. Run the check server.
3. Tell everyone to navigate to the webserver.
4. Enjoy the fruits of wwatching a hundred people program.

I recommend a virtualenv with all the requirements satisfied.
Do not forget to enter the correct check server address in website/settings.py
Also, this might not be the best way to go about the business so please help out.
