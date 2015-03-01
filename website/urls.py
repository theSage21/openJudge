from django.conf.urls import patterns, include, url
from django.contrib import admin
from question import views
urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^question/',include('question.urls',namespace='question')),
    url(r'^scoreboard/$',views.scoreboard,name='scoreboard'),
    #-------
    url(r'^login/$','django.contrib.auth.views.login',name='login'),
    url(r'^logout/$','django.contrib.auth.views.logout',name='logout'),
)
