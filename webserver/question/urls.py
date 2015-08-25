from django.conf.urls import patterns, url


urlpatterns = patterns('question.views',
                       url(r'^leaderboard/$', 'leaderboard', name='leaderboard'),
                       url(r'^$', 'question_home', name='home'),
                       url(r'^(?P<qno>\d+)/$', 'question', name='question'),
                       url(r'^(?P<qno>\d+)/details/$', 'question_details', name='question_details'),
                       url(r'^language/(?P<lno>\d+)/details/$', 'language_details', name='language_details'),
                       url(r'^detail_list/', 'detail_list', name='detail_list'),
                       )
