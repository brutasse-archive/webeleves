# -*- coding: UTF-8 -*-
# URLs for webeleves.trombi
from django.conf.urls.defaults import *
from trombi.views import home

urlpatterns = patterns('',
    # Le trombinoscope
    url(r'^$', home, name='trombi'),
)
