from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import app.views

urlpatterns = [
    url(r'^$', app.views.home),
    url(r'^accueil/$', app.views.home),
    url(r'^article/(?P<article_id>\d+)/$', app.views.article_view),
    url(r'^articles/(?P<year>\d{4})/(?P<month>\d{2})/$', app.views.home),
    url(r'^redirection/$', app.views.redirection_view),
    url(r'^template/$', app.views.tpl)
]

#Debug
urlpatterns += staticfiles_urlpatterns()