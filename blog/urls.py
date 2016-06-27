from django.conf.urls import patterns, url
import blog.views

urlpatterns = [
    url(r'^$', blog.views.home),
    url(r'^accueil/$', blog.views.home),
    url(r'^article/(?P<article_id>\d+)/$', blog.views.article_view),
    url(r'^articles/(?P<year>\d{4})/(?P<month>\d{2})/$', blog.views.article_list),
    url(r'^redirection/$', blog.views.redirection_view),
    url(r'^template/$', blog.views.tpl)
]
