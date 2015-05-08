from django.conf.urls import patterns,include,url


urlpatterns=patterns('contest.views',
    url(r'^$','home',name='home'),
)
