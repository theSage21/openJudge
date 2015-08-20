#! /bin/bash
source ./env/bin/activate
cd openJudge
setup_folder=$PWD
RED='\033[0;31m'
NC='\033[0m' # No Color

#CHECKSERVER SETUP
echo -e "$RED Checkserver Setup started.$NC"
# make check data folders
mkdir check_data
mkdir check_data/wrappers check_data/inputs 
mkdir check_data/outputs check_data/source
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
path = os.path.join( os.path.split(os.getcwd())[0], 'check_data', 'wrappers')
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
echo 'Completed setup. Wrapping up'
python3 data_creator.py
echo -e "$RED ==================================================== $NC"
rm data_creator.py
rm -rf calibration
