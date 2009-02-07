# Main website
from django.shortcuts import render_to_response
from website.models import ArticleForm
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

@login_required
def suggest(request):
    form = ArticleForm()
    return render_to_response('website/suggest.html', locals(), context_instance=RequestContext(request))
