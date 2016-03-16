from django.conf.urls import patterns, url

urlpatterns = patterns('blog.views',
    url(r'^accueil/$', 'home'),
    url(r'^article/(\d+)/$', 'article_view'),
    url(r'^article/(\d{4})/(\d{2})/$', 'article_list'),
	)
