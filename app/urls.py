from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import app.views

app_name = 'app'

urlpatterns = [
    url(r'^$', app.views.home, name='index'),
    url(r'^accueil/$', app.views.home, name='home'),
    url(r'^article/(?P<article_id>\d+)/$', app.views.article_view, name='article_view'),
    url(r'^articles/(?P<year>\d{4})/(?P<month>\d{2})/$', app.views.home, name='article_list'),
    url(r'^rummage_list/(?P<user_id>\d+)/$', app.views.rummage_list, name='rummage_list'),
    url(r'^rummage/(?P<rummage_id>\d+)/$', app.views.rummage, name='rummage'),
    url(r'^rummage_add/$', app.views.rummage_add, name='rummage_add'),
    url(r'^redirection/$', app.views.redirection_view, name='redirection'),
    url(r'^template/$', app.views.tpl, name='template'),
    
]

#Debug
urlpatterns += staticfiles_urlpatterns()