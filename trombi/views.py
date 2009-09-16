# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from shortcuts import render
from trombi.forms import MainProfileForm, NetworkForm, ScholarshipForm

@login_required
def trombi(request):
    """Homepage of the Trombi app"""
    return render(request, 'trombi/main.html', locals())

@login_required
def promo(request, promo):
    """Lists all students of a specific year"""
    pass

@login_required
def eleve(request, promo, login):
    """Public profile of this guy"""
    pass

@login_required
def profile(request):
    profile = request.user.get_profile()
    return render(request, 'trombi/profile.html', locals())

@login_required
def edit_profile(request):
    """Editing the profile"""
    profile = request.user.get_profile()
    if request.method == 'POST':
        form = MainProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            request.user.message_set.create(message='Your profile has been updated')
            url = reverse('trombi:profile')
            return redirect(url)
    else:
        form = MainProfileForm(instance=profile)
    return render(request, 'trombi/edit_profile.html', locals())

@login_required
def edit_profile_networks(request):
    profile = request.user.get_profile()
    if request.method == 'POST':
        form = NetworkForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            request.user.message_set.create(message='Your profile has been updated')
            url = reverse('trombi:profile')
            return redirect(url)
    else:
        form = NetworkForm(instance=profile)
    return render(request, 'trombi/edit_network_profile.html', locals())

@login_required
def edit_profile_school(request):
    profile = request.user.get_profile()
    if request.method == 'POST':
        form = ScholarshipForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            request.user.message_set.create(message='Your profile has been updated')
            url = reverse('trombi:profile')
            return redirect(url)
    else:
        form = ScholarshipForm(instance=profile)
    return render(request, 'trombi/edit_school_profile.html', locals())

@login_required
def search(request):
    """Make a search with lots of criteria"""
    pass

@login_required
def browse(request):
    """List all promos"""
    pass
