from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
                       url(r'^', include('contest.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^question/', include('question.urls', namespace='question')),
                       url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login'),
                       url(r'^logout/$', 'django.contrib.auth.views.logout',
                           {'template_name': 'logout.html'}, name='logout'),
                       )
