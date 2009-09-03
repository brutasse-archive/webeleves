# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from shortcuts import render

@login_required
def trombi(request):
    return render(request, 'trombi/main.html', locals())
