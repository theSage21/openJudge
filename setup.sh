#! /bin/bash
RED='\033[0;31m'
NC='\033[0m' # No Color

if source ./env/bin/activate; then
    echo "Virtualenv found"
else
    virtualenv -p python3 env
    source env/bin/activate
fi
pip install -r requirements.txt

setup_folder=$PWD
echo $setup_folder
# add absolute path to the wrappers

echo -e "$RED Webserver Setup started.$NC"
# WEBSERVER SETUP
cd openjudge
rm db.sqlite3 
rm -rf static_files

python manage.py makemigrations
python manage.py migrate
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
import django
django.setup()
from contest import models
from django.core.files import File
from datetime import timedelta

print('Adding contest')
contest = models.Contest()
contest.name = 'Practice'
contest.save()

print('Adding wrappers')
path = os.path.join(os.path.split(os.getcwd())[0], 'wrappers')
wrappers = os.listdir(path)
for wr in wrappers:
    if 'input.py' == wr:
        continue
    ln = models.Language()
    ln.name=wr[:-3]
    ln.wrapper = File(open(os.path.join(path, wr),'r'))
    if 'java' in wr.lower():
        ln.strict_filename = True
    ln.save()

print('Adding calibration questions')
q = models.Question()
q.title='Square It- Calibration'
q.text = '''Read 5 integers from stdin (cin, scanf, input etc).\nFor each integer read print it's square on a seperate line.
Keep in mind that if you print unnecessary things like 'Enter a number: ' and 'answer is: ', your attempt will be
considered wrong.

Only print what is required.

Example:
-------
1
2
3
4
5

1
4
9
16
25
'''
q.contest = contest
q.save()

print('Adding answers for questions')
a= models.TestCase()
a.question = q
a.inp = File(open('calibration/inp', 'r'))
a.out= File(open('calibration/out', 'r'))
a.exact_check = True
a.save()

print('Adding dummy user')
u = models.User()
u.username = 'dummy'
u.set_password('asd')
u.save()

p = models.Profile()
p.user=u
p.contest = contest
p.save()
print('\033[0;31m Username: dummy \033[0m')
print('\033[0;31m Password: asd \033[0m')
" > data_creator.py
python3 data_creator.py
echo 'Completed setup. Wrapping up'
echo -e "$RED ==================================================== $NC"
rm data_creator.py
rm -rf calibration
