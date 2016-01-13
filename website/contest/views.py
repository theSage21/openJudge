from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
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



@login_required
def question(request, cpk, qpk):
    context = {}
    template = 'contest/question.html'

    context['contest'] = get_object_or_404(models.Contest, pk=cpk)
    context['question'] = get_object_or_404(models.Question, pk=qpk)
    profile_user = models.Profile.objects.filter(user=request.user)
    profile = profile_user.filter(contest=context['contest'])[0]

    if request.method == 'GET':
        
        context['answer_form'] = models.AttemptForm()
    elif request.method == 'POST':
        form = models.AttemptForm(request.POST, request.FILES)
        if form.is_valid():
            attempt = form.save(commit=False)
            attempt.profile = profile
            attempt.question = context['question']
            attempt.save()
        else:
            data['answer_form'] = form
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
