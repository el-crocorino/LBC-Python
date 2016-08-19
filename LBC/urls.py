from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from app import views as app_views

urlpatterns = [
    # Examples:
    # url(r'^$', 'LBC.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    url(r'^accounts/login/$', auth_views.login, {'template_name': 'app/login.html'}, name='login'),
    url(r'^accounts/logout/$', auth_views.logout,  {'next_page': '/app/rummage_list/'}, name='logout'),
    url(r'^accounts/register/$', app_views.register, name='register'),
    url(r'^accounts/register/success/$', app_views.register_success, name='register_success'),    
    url(r'^admin/', admin.site.urls),
    url(r'^blog/', include('blog.urls', namespace="blog")),
    url(r'^app/', include('app.urls', namespace="app")),
]
