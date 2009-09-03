# -*- coding: UTF-8 -*-
from django.conf.urls.defaults import *
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect

# Admin
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Admin documentation
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Admin
    (r'^admin/', include(admin.site.urls)),

    (r'^trombi/', include('trombi.urls', namespace='trombi')),
    (r'^photos/', include('photos.urls', namespace='photos')),
    (r'^forum/', include('forum.urls', namespace='forum')),

    # Le site principal
    (r'^', include('website.urls')),

    # Robots et favicon pour navigateurs débiles
    url(r'^robots.txt$', lambda _:
        HttpResponse('User-agent: *\nDisallow:\n', mimetype='text/plain')),
    url(r'^favicon.ico$',   lambda _:
        HttpResponseRedirect('%sfavicon.png' % settings.MEDIA_URL)),
)

if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
            url(r'^static/(?P<path>.*)$', 'serve',
                {'document_root': settings.MEDIA_ROOT}),
    )
