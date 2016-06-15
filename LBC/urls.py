from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = ['',
    # Examples:
    # url(r'^$', 'LBC.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include('blog.urls')),
    url(r'^app/', include('app.urls')),
]
