from shortcuts import render
from website.models import ArticleForm
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

@login_required
def suggest(request):
    form = ArticleForm()
    return render(request, 'website/suggest.html', locals(), context_instance=RequestContext(request))
