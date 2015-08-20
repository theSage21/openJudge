from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static

urlpatterns = patterns('',
                       url(r'^', include('contest.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^question/', include('question.urls', namespace='question')),
                       url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login'),
                       url(r'^logout/$', 'django.contrib.auth.views.logout',
                           {'template_name': 'logout.html'}, name='logout'),
                       ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
