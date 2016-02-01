from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from contest import models
from contest.forms import AttemptForm, RegistrationForm, ProfileForm

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


@login_required
def question(request, cpk, qpk):
    context = {}
    template = 'contest/question.html'

    context['contest'] = get_object_or_404(models.Contest, pk=cpk)
    context['question'] = get_object_or_404(models.Question, pk=qpk)

    if not context['contest'].live:
        return redirect('contest', cpk=context['contest'].pk)

    profile_user = models.Profile.objects.filter(user=request.user)
    try:
        profile = profile_user.filter(contest=context['contest'])[0]
    except IndexError:
        return redirect('not_registered')
    last_attempt = profile.profile_attempt.filter(question=context['question']).order_by('-stamp').first()
    context['last_attempt'] = last_attempt

    if request.method == 'GET':
        context['answer_form'] = AttemptForm(instance=last_attempt) if last_attempt else AttemptForm()
    elif request.method == 'POST':
        form = AttemptForm(request.POST, request.FILES)
        if form.is_valid():
            attempt = form.save(commit=False)
            attempt.profile = profile
            attempt.question = context['question']
            attempt.save()
            return redirect('question', cpk=cpk, qpk=qpk)
        else:
            context['answer_form'] = form
    return render(request, template, context)

def signup(request):
    context = {}
    template = 'contest/signup.html'
    context['form'] = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            uname = form['username'].value()
            pwd = form['password'].value()
            p = models.User()
            p.username = uname
            p.set_password(pwd)
            p.save()
            context['successful_registration'] = uname
            return redirect('login')
        else:
            context['form'] = form
    return render(request, template, context)

@login_required
def register(request):
    context = {}
    template = 'contest/register.html'
    context['form'] = ProfileForm()
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            if models.Profile.objects.filter(user=profile.user, contest=profile.contest).count() == 0:
                profile.save()
                context['successful_registration'] = profile.user
            return redirect('contest', cpk=profile.contest.pk)
        else:
            context['form'] = form
    return render(request, template, context)


def leaderboard(request, cpk):
    context = {}
    template = 'contest/leaderboard.html'
    con = get_object_or_404(models.Contest, pk=cpk)
    players = [i for i in  models.Profile.objects.filter(contest=con)]
    players.sort(key=lambda x:x.score, reverse=True)
    # This seems neater to me
    context['players'] = players
    context['contest'] = get_object_or_404(models.Contest, pk=cpk)
    return render(request, template, context)


def not_registered(request):
    context = {}
    template = 'contest/not_reg.html'
    return render(request, template, context)
