from django.views.generic.base import TemplateView
from django.conf.urls import patterns, include, url
from django.shortcuts import render
from django.contrib import admin
from django.conf import settings
import datetime

def home(request):
    data={}
    data['time']=settings.START_TIME+datetime.timedelta(0,60*60*3,0)
    return render(request,'base.html',data)

urlpatterns = patterns('',
    url(r'^$',home,name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^question/',include('question.urls',namespace='question')),
    url(r'^scoreboard/$','question.views.scoreboard',name='scoreboard'),
    #-------
    url(r'^login/$','django.contrib.auth.views.login',name='login'),
    url(r'^logout/$','django.contrib.auth.views.logout',name='logout'),
)
