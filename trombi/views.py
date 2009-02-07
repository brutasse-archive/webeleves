# Trombi views
from django.shortcuts import render_to_response
from django.template import RequestContext

def home(request):
    return render_to_response('trombi/main.html', locals(), context_instance=RequestContext(request))
