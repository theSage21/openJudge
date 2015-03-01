from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from question import models

def home(request):
    data={}
    template='question/home.html'
    data['questions']=models.Question.objects.all()
    return render(request,template,data)

@login_required
def quest(request,q_no):
    data={}
    template='question/question.html'
    data['questions']=models.Question.objects.all()
    q_no=int(q_no)
    question=get_object_or_404(models.Question,pk=q_no)
    data['question']=question
    data['attempt_form']=models.AttemptForm()
    data['attempts']=models.Attempt.objects.filter(player=request.user,question=question).order_by('stamp')
    if request.method=='POST':
        form=models.AttemptForm(request.POST,request.FILES)
        if form.is_valid():
            attempt=form.save(commit=False)
            attempt.player=request.user.player
            attempt.question=question
            attempt.save()
            attempt.check_attempt()
        else:
            data['attempt_form']=form
    return render(request,template,data)

def scoreboard(request):
    data={}
    template='question/scoreboard.html'
    data['players']=models.Player.objects.all().order_by('score').values('teamname')
    return render(request,template,data)
