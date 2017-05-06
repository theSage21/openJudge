from django.db import models as M
from django.db.models import Sum
from django.contrib.auth.models import User


class Language(M.Model):
    name = M.CharField(max_length=100)
    bash_wrap = M.TextField()

class Contest(M.Model):
    title = M.CharField(max_length=100)
    start = M.DateTimeField()
    end = M.DateTimeField()


class Question(M.Model):
    title = M.CharField(max_length=100)
    text = M.TextField()
    contest = M.ForeignKey('Contest', related_name='contest_question')


class TestCase(M.Model):
    inp_file = M.FileField()
    out_file = M.FileField()
    marks_on_pass = M.FloatField(default=1)
    question = M.ForeignKey('Question', related_name='question_testcase')


class Participant(M.Model):
    user = M.ForeignKey(User, related_name='user_participant')
    contest = M.ForeignKey('Contest', related_name='contest_participant')
    nick = M.CharField(max_length=50)

    def get_score(self):
        # Get the attempts this person made
        # Filter: assessed, counted, belongs to this contest
        attempts = self.participant_attempt.filter(question__contest=self.contest,
                    assessed=True,
                    counted_for_score=True)
        # Sum of scores obtained
        total_score = attempts.aggregate(Sum('score_obtained'))
        return total_score


class Attempt(M.Model):
    code = M.TextField()
    language = M.ForeignKey('Language', related_name='language_attempt')
    question = M.ForeignKey('Question', related_name='question_attempt')
    participant = M.ForeignKey('Participant', related_name='participant_attempt')
    assessed = M.BooleanField(default=False)
    valid = M.BooleanField(default=False)
    counted_for_score = M.BooleanField(default=True, help_tex_textt='Multiple good attempts should not increase score')
    score_obtained = M.FloatField(default=0)

    submission_time = M.DateTimeField(auto_now_add=True)

    def assess_this_attempt(self):
        # TODO
        pass
