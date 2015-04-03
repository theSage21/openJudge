from django.conf.urls import patterns,include,url


urlpatterns=patterns('player.views',
    url(r'^$','home',name='home'),
    url(r'^leaderboard/$','leaderboard',name='leaderboard'),
    url(r'^question/$','question_home',name='question_home'),
    url(r'^question/(?P<qno>\d+)/$','question',name='question'),
    url(r'^question/(?P<qno>\d+)/details/$','question_details',name='question_details'),
    url(r'^language/(?P<lno>\d+)/details/$','language_details',name='language_details'),
)
