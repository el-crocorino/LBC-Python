from django.conf.urls import patterns, url

urlpatterns = ['app.views',
    url(r'^accueil/$', 'home'),
    url(r'^article/(?P<article_id>\d+)/$', 'article_view'),
    url(r'^articles/(?P<year>\d{4})/(?P<month>\d{2})/$', 'article_list'),
    url(r'^redirection/$', 'redirection_view'),
    url(r'^$', 'tpl')
]
