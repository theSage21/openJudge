from django.shortcuts import render


def home(request):
    data = {}
    template = 'contest/home.html'
    return render(request, template, data)
