from django.conf.urls import url
from contests import views as V

urlpatterns = [
    url(r'^contest/all/$', V.contests),
    url(r'^contest/(?P<contest_pk>[0-9]+)/$', V.contest_home),
    url(r'^contest/(?P<contest_pk>[0-9]+)/leader/$', V.contest_leader),
    url(r'^contest/(?P<contest_pk>[0-9]+)/(?P<question_pk>[0-9]+)/$', V.question),
]
