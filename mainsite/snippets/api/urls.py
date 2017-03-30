from django.conf.urls import url
from django.contrib import admin
from rest_framework import renderers
from rest_framework.urlpatterns import format_suffix_patterns


from .views import (
    SnippetList,
    UserViewSet,
    SnippetCreateAPIView,
    SnippetListAPIView,
    SnippetViewSet,
  #  SnippetDetailView,
    SnippetDetailAPI2,
    UserListAPIView,
    UserDetailAPIView,
    SnippetHighlight,
    api_root
)

snippet_list = SnippetViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })

snippet_detail = SnippetViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

user_list = UserViewSet.as_view({
    'get': 'list'
})

user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})


urlpatterns = [
    # url(r'^$', views.api_root),
    url(r'^create/$', SnippetCreateAPIView.as_view(), name='create'),
    url(r'^list/$', SnippetListAPIView.as_view(), name='list'),
    url(r'^list2/$', SnippetList.as_view(), name='list2'),
    url(r'^detail/(?P<pk>[0-9]+)/$', SnippetDetailAPI2.as_view(), name='detail'),
    url(r'^highlight/(?P<pk>[0-9]+)/$', SnippetHighlight.as_view(), name='snippet-highlight'),
    url(r'^users/$', UserListAPIView.as_view(), name='list'),
    url(r'users/(?P<pk>[0-9]+)/$', UserDetailAPIView.as_view(), name='user-detail')
]

# urlpatterns = format_suffix_patterns([
#     url(r'^$', api_root),
#     url(r'^list/$', snippet_list, name='snippet-list'),
#     url(r'^detail/(?P<pk>[0-9]+)/$', snippet_detail, name='snippet-detail'),
#    # url(r'^snippets/(?P<pk>[0-9]+)/highlight/$', snippet_highlight, name='snippet-highlight'),
#     url(r'^users/$', user_list, name='user-list'),
#     url(r'^users/(?P<pk>[0-9]+)/$', user_detail, name='user-detail')
# ])


