from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'snippets/$', snippet_list),
    url(r'snippet/(?P<pk>[0-9]+)/$', snippet_detail),

]