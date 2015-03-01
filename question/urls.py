from django.conf.urls import patterns,include,url
from question import views

urlpatterns=patterns('',
    url(r'^$',views.home,name='home'),
    url(r'^(?P<q_no>\d+)/$',views.quest,name='question'),
    url(r'^score/$',views.scoreboard,name='scoreboard'),
)
