from django.db import models
from socket import create_connection
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from contest.utils import is_correct


class Contest(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=50)
    live = models.BooleanField(default=True)
    published = models.BooleanField(default=True)
    timeout = models.FloatField(default=6.0)
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
            #val = is_correct(self)
            val = True
            # TODO
            if val is not None:  # avoid DB hit if None
                self._correct = val
                self.save()
        return val
    correct = property(_get_correct)

    def _get_marks(self):
        on_this_question = Attempt.objects.filter(question=self.question)
        before_this = on_this_question.filter(stamp__lt=self.stamp)
        wrong = sum((1 for i in before_this if i.correct == False))
        total = sum((1 for i in before_this if i.correct is not None))
        result = 1 if total == 0 else float(wrong) / total
        return result
    marks = property(_get_marks)
