# -*- coding: UTF-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('django.contrib.auth.views',
    # Login / logout
    url(r'^login/$', 'login', name='login'),
    url(r'^logout/$', 'logout', name='logout'),
)

urlpatterns += patterns('website.views',
    # Le site principal
    url(r'^$', 'home', name='home'),
    url(r'^articles/proposer/$', 'suggest', name='proposer_article'),
    url(r'^articles/(?P<slug>[-\w]+)/$', 'article', name='article'),
)
