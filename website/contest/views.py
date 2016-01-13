from django.shortcuts import render, get_object_or_404
from contest import models

def home(request):
    context = {}
    template = 'contest/home.html'
    context['contests'] = models.Contest.objects.filter(published=True)
    return render(request, template, context)


def contest(request, cpk):
    context = {}
    template = 'contest/contest.html'
    contest = get_object_or_404(models.Contest, pk=cpk)
    context['contest'] = contest
    context['questions'] = models.Question.objects.filter(contest=contest)
    return render(request, template, context)


def details(request, cpk):
    context = {}
    template = 'contest/contest.html'
    return render(request, template, context)



def question(request, cpk, qpk):
    context = {}
    template = 'contest/question.html'
    q = get_object_or_404(models.Question, pk=qpk)
    context['contest'] = get_object_or_404(models.Contest, pk=cpk)
    context['question'] = q
    if request.method == 'GET':
        form = None
        # TODO  show form
    elif request.method == 'POST':
        form = None
        # TODO  accept form
    return render(request, template, context)


def register(request):
    context = {}
    template = 'contest/register.html'
    # TODO
    return render(request, template, context)


def leaderboard(request, cpk):
    context = {}
    template = 'contest/leaderboard.html'
    con = get_object_or_404(models.Contest, pk=cpk)
    players = [i for i in  models.Profile.objects.filter(contest=con)]
    players.sort(key=lambda x:x.score)
    # This seems neater to me
    context['players'] = players
    context['contest'] = get_object_or_404(models.Contest, pk=cpk)
    return render(request, template, context)
