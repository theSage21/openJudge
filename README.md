OpenJudge
=========

A judge I made to judge the simple programming competitions in college.
A django based web server to provide the interface.
A linux shell based python mashup to provide the checking of the code.
=======
Supports python3,python2,java,c++,c.
Serves a webserver using Django.
Checks the code via simple shell script wrappers and pipes and output comparison.

Setup
-----
It is important that the webserver is running before the cehckserver is set up.
Set the CHECK_SERVER_ADDRESS in settings.py

The webserver is set up as a standard django server. I prefer using Nginx,Gunicorn as a 
combination.

Run slave.py on a linux like machine. It will ask for the webserver address. Provide as shown in example.

Usage
------

1. Register users with question.models.nplayer()
2. Run the webserver. Run the check server.

I recommend a virtualenv with all the requirements satisfied.
Do not forget to enter the correct check server address in website/settings.py
