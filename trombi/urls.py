# -*- coding: UTF-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('trombi.views',
    url(r'^$', 'trombi', name='trombi'),
)
