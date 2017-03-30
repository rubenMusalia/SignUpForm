from django.conf.urls import url
from django.contrib import admin

from .views import (
    ProfileListAPIView,
    ProfileDetailAPIView,
    ProfileDeleteView,
   # ProfileUpdateAPIView,
    ProfileCreateAPIView,
    CreateUserAPIView,
    UserLoginAPIView
     )

urlpatterns = [
    url(r'^users/register$', CreateUserAPIView.as_view(), name='register'),
    url(r'^users/login/$', UserLoginAPIView.as_view(), name='login'),

    url(r'^users/list/$', ProfileListAPIView.as_view(), name='list'),
    # url(r'^user/create/$', ProfileCreateAPIView.as_view(), name='create'),
    url(r'^users/detail/(?P<pk>[\w-]+)/$', ProfileDetailAPIView.as_view(), name='detail'),
   # url(r'^users/edit/(?P<pk>[\w-]+)/$', ProfileUpdateAPIView.as_view(), name='edit'),
    url(r'^users/delete/(?P<pk>[\w-]+)/$', ProfileDeleteView.as_view(), name='delete')
]