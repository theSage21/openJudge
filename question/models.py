from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django import forms
from question import functions


class Player(User):
    score=models.IntegerField(default=0)
    teamname=models.CharField(max_length=100)
    def calculate_score(self):
        #since sqlite3 does not support distinct
        #otherwise
        #count=Attempt.objects.fitler(player=self,correct=True).order_by('question').distinct('question').count()
        attempts=Attempt.objects.filter(player=self,correct=True)
        q_done=[]
        count=0
        for att in attempts:
            if att.question not in q_done:
                q_done.append(att.question)
                count+=1
        self.score=count
        self.save()

class Question(models.Model):
    def __str__(self):return str(self.id)+str(self.text[:20])+' ...'
    text=models.TextField()
    test_file=models.FileField(upload_to='test_file')
    def get_absolute_url(self):
        return reverse('question:question',kwargs={'q_no':self.id})
class Language(models.Model):
    def __str__(self):return self.name
    name=models.CharField(max_length=100)
    wrapper=models.FileField(upload_to='wrappers')

class Attempt(models.Model):
    def __str__(self):return self.player.__str__()+self.question.__str__()
    question=models.ForeignKey(Question,related_name='question_attempt')
    player=models.ForeignKey(Player,related_name='player_attempt')
    source=models.FileField()
    correct=models.NullBooleanField(default=None)
    traceback=models.TextField(blank=True)
    language=models.ForeignKey(Language,related_name='attempt_language')
    #-----------------------------------
    stamp=models.DateTimeField(auto_now_add=True)#timestamp of attempt

    def check_attempt(self):
        print('Checking attempt')
        #------------------
        testpath=self.question.test_file.path
        codepath=self.source.path
        print(testpath)
        print(codepath)
        ck_ser=functions.CheckServer(codepath,testpath,self.language.wrapper.path,self.pk)
        run_success,feedback=ck_ser.run()
        self.correct=run_success
        if not run_success:self.traceback=feedback
        self.save()
        #----------------------
    def is_correct(self):
        if self.correct!=None:return self.correct#if code has already been run and tested
        if self.check_attempt():self.correct=True
        else:self.correct=False
        self.save()
        return self.correct
    class Meta:
        ordering=['correct','stamp']

class AttemptForm(forms.ModelForm):
    class Meta:
        model=Attempt
        fields=['source','language']
        
def nplayer():
    p=Player()
    p.teamname=input('TeamName:')
    p.username=p.teamname
    p.set_password(input('Password:'))
    p.save()
