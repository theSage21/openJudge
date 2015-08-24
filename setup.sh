#! /bin/bash
RED='\033[0;31m'
NC='\033[0m' # No Color

if source ./env/bin/activate; then
    echo "Virtualenv found"
else
    virtualenv -p python3 env
    source env/bin/activate
fi

setup_folder=$PWD

#CHECKSERVER SETUP
echo -e "$RED Checkserver Setup started.$NC"
# make check data folders
mkdir check_data
mkdir check_data/wrappers check_data/inputs 
mkdir check_data/outputs check_data/source
mkdir check_data/temp
# copy wrappers to the appropriate folders
cp wrappers/* check_data/wrappers/
# add absolute path to the wrappers

echo -e "$RED Webserver Setup started.$NC"
# WEBSERVER SETUP
cd webserver
rm db.sqlite3 
rm -rf staticfiles
rm -rf static_files

python manage.py makemigrations
python manage.py migrate
mkdir staticfiles
python manage.py collectstatic --noinput
echo -e "$RED Set up a superuser. $NC"
python manage.py createsuperuser
echo -e "$RED Setting up languages and questions. $NC"
mkdir calibration
cd calibration
echo "1
2
3
4
5">inp
echo "1
4
9
16
25">out
echo "
for i in range(5):
    x = input()
    x = int(x)
    print(x*x)" > sample

cd ..
echo "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
from question import models
from django.core.files import File
import django
django.setup()

print('Adding answer types')
at = models.AnswerType()
at.name='Error Range'
at.save()
at = models.AnswerType()
at.name='Exact'
at.save()

print('Adding wrappers')
path = os.path.join(os.path.split(os.getcwd())[0], 'check_data', 'wrappers')
wrappers = os.listdir(path)
for wr in wrappers:
    if 'input.py' == wr:
        continue
    ln = models.Language()
    ln.name=wr[:-3]
    ln.details = wr
    ln.wrapper = File(open(os.path.join(path, wr),'r'))
    ln.save()

print('Adding calibration questions')
q = models.Question()
q.qno = 0
q.title='Square It- Calibration'
q.text = 'This is a calibration question. Square the input provided (5 numbers)'
q.save()

print('Adding answers for questions')
a= models.Answer()
a.question = q
a.infile = File(open('calibration/inp', 'r'))
a.outfile = File(open('calibration/out', 'r'))
a.sample_code = File(open('calibration/sample', 'r'))
a.answer_type = at
a.save()

print('Adding dummy user')
p = models.Profile()
p.username='dummy'
p.set_password('asd')
p.save()
print('\033[0;31m Username: dummy \033[0m')
print('\033[0;31m Password: asd \033[0m')
" > data_creator.py
python3 data_creator.py
echo 'Completed setup. Wrapping up'
echo -e "$RED ==================================================== $NC"
rm data_creator.py
rm -rf calibration

echo -e "$RED Installing Nginx $NC"

sudo apt-get install nginx
sudo service nginx start

echo "
upstream app_server_djangoapp {
    server unix:$setup_folder/gunicorn_socket fail_timeout=0;
}
server {
    listen 0.0.0.0:80;
    server_name  .example.com;
 
    keepalive_timeout 5;
    # path for static files
    root $setup_folder/webserver/static_files/;" > $setup_folder
echo '    location / {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        if (!-f $request_filename) {
            proxy_pass http://app_server_djangoapp;
            break;
        }
    }
}' >> $setup_folder
sudo mv $setup_folder /etc/nginx/sites-available/openJudge

cd /etc/nginx/sites-enabled/
sudo ln /etc/nginx/sites-available/openJudge
sudo service nginx reload

echo -e "$PWD Completed Nginx setup $NC"

cd $setup_folder
sed -i "s/LOCATION/$setup_folder/" runserver.sh
pip install -r requirements.txt
