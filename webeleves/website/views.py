# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.views.generic.list_detail import object_list, object_detail

from datetime import datetime

from shortcuts import render
from website.models import Article, ArticleForm, Event

def get_qs_for_user(user):
    """Depending on the user (anonymous / authenticated), some articles will or
    will not be shown. This is the place where the filtering is done"""
    if user.is_authenticated():
        return Article.objects.private()
    else:
        return Article.objects.public()

def home(request):
    """Home page"""
    articles = get_qs_for_user(request.user)
    events = Event.objects.filter(date__gte=datetime.today())
    if request.user.has_perm('website.add_event'):
        request.user.can_add_event = True
    return render(request, 'website/home.html', locals())

def news(request):
    """Recent articles with pagination"""
    qs = get_qs_for_user(request.user)
    return object_list(request, qs, paginate_by=5)

def article(request, slug):
    """Deal with permissions and display the article"""
    qs = get_qs_for_user(request.user)
    if request.user.has_perm('comments.add_comment'):
        request.user.can_comment = True
    return object_detail(request, qs, slug=slug)

@login_required
def suggest(request):
    form = ArticleForm()
    return render(request, 'website/suggest.html', locals(), context_instance=RequestContext(request))
