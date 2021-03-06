# -*- coding: UTF-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('trombi.views',
    url(r'^$', 'trombi', name='trombi'),
    url(r'^search/$', 'search', name='search'),
    url(r'^contest/$', 'contest', name='contest'),
    url(r'^opensearch/$', 'opensearch', name='opensearch'),
    url(r'^profile/$', 'profile', name='profile'),
    url(r'^profile/edit/$', 'edit_profile', name='edit_profile'),
    url(r'^profile/edit/networks/$', 'edit_profile_networks',
        name='edit_profile_networks'),
    url(r'^profile/edit/school/$', 'edit_profile_school',
        name='edit_profile_school'),
    url(r'^promo(?P<promo>\d{4})/$', 'promo', name='promo'),
    url(r'^promo(?P<promo>\d{4})/(?P<login>[^/]+)/$', 'eleve', name='eleve'),
    url(r'^promo(?P<promo>\d{4})/(?P<login>[^/]+)/vcard/$', 'vcard', name='vcard'),
)
