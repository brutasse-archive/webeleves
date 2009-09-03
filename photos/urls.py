# -*- coding: UTF-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('photos.views',
    url(r'^$', 'photos', name='photos'),
)
