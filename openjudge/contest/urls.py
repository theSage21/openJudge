from django.conf.urls import url
from contest import views

urlpatterns = [url(r'^$', views.home, name='home'),
               url(r'^signup/$', views.signup, name='signup'),
               url(r'^register/$', views.register, name='register'),
               url(r'^not_registered/$', views.not_registered, name='not_registered'),
               url(r'^(?P<cpk>\d+)/$', views.contest, name='contest'),
               url(r'^(?P<cpk>\d+)/(?P<qpk>\d+)/$', views.question, name='question'),
               url(r'^(?P<cpk>\d+)/leader/$', views.leaderboard, name='leaderboard'),
               ]
