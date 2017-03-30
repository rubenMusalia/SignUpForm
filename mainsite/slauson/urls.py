from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.BasePageView.as_view(), name='basepage'),
    url(r'^home/$', views.HomePageView.as_view(), name='homepage'),
    url(r'^accounts/register/$', views.RegisterPageView.as_view(), name='register'),
    url(r'^accounts/login/$', views.LoginView.as_view(), name='login'),
    url(r'^accounts/logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^accounts/profile/$', views.ProfileUpdateView.as_view(), name='profile'),
    url(r'^accounts/detail/(?P<slug>[\w.@+-]+)/$', views.ProfileDetailView.as_view(), name='detail'),
    url(r'^accounts/list/$', views.ProfilesListView.as_view(), name='list'),

    url(r'^accounts/password_reset/$', auth_views.password_reset, {'template_name': 'accounts/password_reset_form.html'}
        , name='password_reset',),

    url(r'^accounts/password_reset/done/$', auth_views.password_reset_done, {'template_name':
        'accounts/password_reset_done.html'}, name='password_reset_done'),

    url(r'^accounts/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, {'template_name': 'accounts/password_reset_confirm.html'},
        name='password_reset_confirm'),

    url(r'^accounts/reset/done/$', auth_views.password_reset_complete, {'template_name':
        'accounts/password_reset_done.html'}, name='password_reset_complete'),

]

