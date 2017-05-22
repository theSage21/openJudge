from django.db import models as M
from django.db.models import Sum
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse



class Language(M.Model):
    name = M.CharField(max_length=100)
    bash_wrap = M.TextField()


class Contest(M.Model):
    title = M.CharField(max_length=100)
    start = M.DateTimeField()
    end = M.DateTimeField()
    description = M.TextField()
    link = M.CharField(max_length=200, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('contest', args=[self.pk])


class Question(M.Model):
    title = M.CharField(max_length=100)
    text = M.TextField()
    contest = M.ForeignKey('Contest', related_name='contest_question')

    def get_absolute_url(self):
        return reverse('question', args=[self.contest.pk, self.pk])

    def __str__(self):
        return self.title


class TestCase(M.Model):
    inp_text = M.TextField()
    out_text = M.TextField()
    marks_on_pass = M.FloatField(default=1)
    question = M.ForeignKey('Question', related_name='question_testcase')


class Participant(M.Model):
    user = M.ForeignKey(User, related_name='user_participant')
    contest = M.ForeignKey('Contest', related_name='contest_participant')
    nick = M.CharField(max_length=50, help_text='Will be displayed on leaderboard')

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
    counted_for_score = M.BooleanField(default=True, help_text='Multiple good attempts should not increase score')
    score_obtained = M.FloatField(default=0)

    submission_time = M.DateTimeField(auto_now_add=True)

    def assess_this_attempt(self):
        # ASSESS
        self.is_valid = True  # TODO: Make this a function
        # IS COUNTED?
        how_many_correct_attempts_before_this = Attempt.objects.filter(question=self.question,
                participant=self.participant,
                assessed=True,
                counted_for_score=True,
                submission_time__lt=self.submission_time).count()
        if how_many_correct_attempts_before_this > 0:
            self.counted_for_score = False
        else:
            if self.is_valid:
                self.counted_for_score = True
                test_cases_passed = TestCase.objects.filter(question=self.question)
                self.score_obtained = test_cases_passed.aggregate(Sum('marks_on_pass'))
        self.save()
