from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import app.views

app_name = 'app'

urlpatterns = [
    url(r'^$', app.views.home, name='index'),
    url(r'^accueil/$', app.views.home, name='home'),
    url(r'^article/(?P<article_id>\d+)/$', app.views.article_view, name='article_view'),
    url(r'^articles/(?P<year>\d{4})/(?P<month>\d{2})/$', app.views.home, name='article_list'),
    
    url(r'^rummage/(?P<rummage_id>\d+)/$', app.views.rummage, name='rummage'),
    url(r'^rummage_list/(?P<user_id>\d+)/$', app.views.rummage_list, name='rummage_list'),
    url(r'^rummage_add/$', app.views.rummage_add, name='rummage_add'),
    url(r'^rummage_delete/(?P<rummage_id>\d+)/$', app.views.rummage_delete, name='rummage_delete'),
    url(r'^rummage_update/(?P<rummage_id>\d+)/$', app.views.rummage_update, name='rummage_update'),
    
    url(r'^criteria/(?P<criteria_id>\d+)/$', app.views.criteria, name='criteria'),
    url(r'^criteria_list/(?P<rummage_id>\d+)/$', app.views.criteria_list, name='criteria_list'),
    url(r'^criteria_add/(?P<rummage_id>\d+)/$', app.views.criteria_add, name='criteria_add'),
    url(r'^criteria_delete/(?P<criteria_id>\d+)/$', app.views.criteria_delete, name='criteria_delete'),
    url(r'^criteria_update/(?P<criteria_id>\d+)/$', app.views.criteria_update, name='criteria_update'),
    
    url(r'^rummage_item/(?P<rummage_item_id>\d+)/$', app.views.rummage_item, name='rummage_item'),
    url(r'^rummage_item_list/(?P<rummage_id>\d+)/$', app.views.rummage_item_list, name='rummage_item_list'),
    url(r'^rummage_item_add/(?P<rummage_id>\d+)/$', app.views.rummage_item_add, name='rummage_item_add'),
    url(r'^rummage_item_delete/(?P<rummage_item_id>\d+)/$', app.views.rummage_item_delete, name='rummage_item_delete'),
    url(r'^rummage_item_update/(?P<rummage_item_id>\d+)/$', app.views.rummage_item_update, name='rummage_item_update'),
    
    url(r'^redirection/$', app.views.redirection_view, name='redirection'),
    url(r'^template/$', app.views.tpl, name='template'),
    
]

#Debug
urlpatterns += staticfiles_urlpatterns()