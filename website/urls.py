# -*- coding: UTF-8 -*-
# URLs for webeleves.website
from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout
from website.views import suggest
from website.models import Article

info_dict = {
        'queryset': Article.objects.published(),
        'paginate_by': 5,
}
detail_dict = { 'queryset': Article.objects.published(), }

urlpatterns = patterns('',
    # Login / logout
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    # Le site principal
    url(r'^$', 'django.views.generic.list_detail.object_list', info_dict, name='home'),
    url(r'^articles/proposer/$', suggest, name='proposer_article'),
    url(r'^articles/(?P<slug>[-\w]+)/$', 'django.views.generic.list_detail.object_detail', detail_dict, name='article'),
)
