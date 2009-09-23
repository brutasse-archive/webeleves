# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.list_detail import object_list, object_detail
from django.contrib.auth.models import User
from django.db.models import Q

from shortcuts import render
from trombi.models import UserProfile
from trombi.forms import MainProfileForm, NetworkForm, ScholarshipForm, \
        SearchForm

@login_required
def trombi(request):
    """Homepage of the Trombi app"""
    # Promos, most recent first
    promos = UserProfile.objects.distinct().values('promo').order_by('-promo')
    form = SearchForm()
    return render(request, 'trombi/main.html', locals())

@login_required
def promo(request, promo):
    """Lists all students of a specific year"""
    # Listing the profile is easier
    users = UserProfile.objects.select_related().filter(promo=promo).order_by('user__last_name')
    extra_context = {'promo': promo}
    return object_list(request, users, template_name='trombi/user_list.html',
            extra_context=extra_context)

@login_required
def eleve(request, promo, login):
    """Public profile of this guy"""
    user = User.objects.get(username=login)
    profile = user.get_profile()
    if not '%s' % profile.promo == '%s' % promo:
        return redirect(reverse('trombi:eleve', args=[profile.promo, login]))

    extra_context = {'profile': profile}
    return object_detail(request, User.objects.all(), user.id,
            template_name='trombi/profile.html',
            extra_context=extra_context)

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
            request.user.message_set.create(message='Ton profil a été mis à jour')
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
            request.user.message_set.create(message='Ton profil a été mis à jour')
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
            request.user.message_set.create(message='Ton profil a été mis à jour')
            url = reverse('trombi:profile')
            return redirect(url)
    else:
        form = ScholarshipForm(instance=profile)
    return render(request, 'trombi/edit_school_profile.html', locals())

@login_required
def search(request):
    """Make a search with some criteria"""
    query = request.GET.get('q')
    if query == u'Nom, prénom, login, surnom': # the u'' is important!
        return redirect(reverse('trombi:trombi'))
    words = query.split(' ')

    # Build a queryset with these terms
    qs = None
    for word in words:
        this_qs = Q(user__username__iexact=word) | \
                Q(user__first_name__iexact=word) | \
                Q(user__last_name__iexact=word) | \
                Q(surname__iexact=word)
        if qs is None:
            qs = this_qs
        else:
            qs = qs & this_qs

    matches = UserProfile.objects.filter(qs)
    return object_list(request, matches, template_name='trombi/user_list.html')
