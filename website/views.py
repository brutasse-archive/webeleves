# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.views.generic.list_detail import object_list, object_detail

from shortcuts import render
from website.models import Article, ArticleForm

def get_qs_for_user(user):
    """Depending on the user (anonymous / authenticated), some articles will or
    will not be shown. This is the place where the filtering is done"""
    if user.is_authenticated():
        return Article.objects.private()
    else:
        return Article.objects.public()

def home(request):
    """Home page"""
    qs = get_qs_for_user(request.user)
    return object_list(request, qs, paginate_by=5)

def article(request, slug):
    """Deal with permissions and display the article"""
    qs = get_qs_for_user(request.user)
    return object_detail(request, qs, slug=slug)

@login_required
def suggest(request):
    form = ArticleForm()
    return render(request, 'website/suggest.html', locals(), context_instance=RequestContext(request))
