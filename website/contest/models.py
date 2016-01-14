from django.db import models
from socket import create_connection
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from contest.comms import is_correct


class Contest(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=50)
    live = models.BooleanField(default=True)
    published = models.BooleanField(default=True)
    def get_absolute_url(self):
        return reverse('contest', args=[self.pk])
    def get_leaderboard(self):
        return reverse('leaderboard', args=[self.pk])



class Profile(models.Model):
    "A profile is a user participating in a contest"
    def __str__(self):
        return self.user.__str__()
    user = models.ForeignKey(User,related_name='user_profile')
    contest = models.ForeignKey(Contest, related_name='contest_profile')
    allowed = models.BooleanField(default=True)

    def _get_score(self):
        all_att = (i for i in Attempt.objects.filter(profile=self) if i.correct)
        total = sum((i.marks for i in all_att))
        return total
    score = property(_get_score)

class Question(models.Model):
    def __str__(self):
        return self.title
    title = models.CharField(max_length=100)
    contest = models.ForeignKey(Contest, related_name='contest_question')
    text = models.TextField()
    def get_absolute_url(self):
        return reverse('question', args=[self.contest.pk, self.pk])


class TestCase(models.Model):
    def __str__(self):
        return self.question.__str__()
    question = models.ForeignKey(Question, related_name='question_testcase')
    inp = models.FileField(upload_to='testcase')
    out = models.FileField(upload_to='testcase')
    exact_check = models.BooleanField(default=True)


class Language(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=50)
    wrapper = models.FileField(upload_to='wrapper')
    timeout = models.FloatField(default=1.0)
    strict_filename = models.BooleanField(default=False,
                                          help_text='Filename cannot be changed')

class Attempt(models.Model):
    def __str__(self):
        return str(self.pk)
    question = models.ForeignKey(Question, related_name='question_attempt')
    profile = models.ForeignKey(Profile, related_name='profile_attempt')
    language = models.ForeignKey(Language, related_name='language_attempt')
    filename = models.CharField(max_length=50, help_text='Setting this sets formatting in editor + filename for Java')
    source = models.TextField()
    stamp = models.DateTimeField(auto_now_add=True)
    _correct = models.NullBooleanField(default=None)
    def _get_correct(self):
        if self._correct is not None:
            val = self._correct
        else:
            val = is_correct(self)
            if val is not None:  # avoid DB hit if None
                self._correct = val
                self.save()
        return val
    correct = property(_get_correct)

    def _get_marks(self):
        on_this_question = Attempt.objects.filter(question=self.question)
        before_this = on_this_question.filter(stamp__lte=self.stamp)
        correct = before_this.filter(correct=True).count()
        total = before_this.exclude(correct=None).count()
        result = 1 if total == 0 else float(correct) / total
    marks = property(_get_marks)


class Slave(models.Model):
    def __str__(self):
        return self.ip + str(self.port)

    ip = models.GenericIPAddressField()
    port = models.IntegerField()
    busy = models.BooleanField(default=False)

    def is_alive(self):
        addr = (self.ip, self.port)
        try:
            con = create_connection(addr)
        except:
            return False
        else:
            con.sendall('Alive'.encode('utf-8'))
            con.close()
            return True

    def get_address(self):
        return (self.ip, self.port)

    def __enter__(self):
        self.busy = True
        self.save()

    def __exit__(self, exc_type, exc_value, traceback):
        self.busy = False
        self.save()
