from django.shortcuts import render
from contests import models as M

def contests(request):
    template, C = 'contests/home.html', dict()
    return render(request, template, C)


def contest_home(request, contest_pk):
    template, C = 'contests/contest.html', dict()
    return render(request, template, C)


def contest_leader(request, contest_pk):
    template, C = 'contests/leader.html', dict()
    return render(request, template, C)


def question(request, contest_pk, question_pk):
    template, C = 'contests/question.html', dict()
    return render(request, template, C)
