# -*- coding: UTF-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('forum.views',
    url(r'^$', 'forum', name='forum'),
)
