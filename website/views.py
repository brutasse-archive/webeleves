# Main website
from django.shortcuts import render_to_response

def home(request):
    return render_to_response('website/main.html', locals())
