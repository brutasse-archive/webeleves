# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from datetime import datetime

class UserProfile(models.Model):
    # Mandatory fields
    user = models.OneToOneField(User, verbose_name=_('User'))
    promo = models.PositiveIntegerField(_('Promotion'))

    # Not required fields
    bio = models.CharField(_('Bio'), max_length=255, null=True, blank=True)
    surname = models.CharField(_('Surname'), max_length=255, null=True,
            blank=True)
    date_of_birth = models.DateField(_('Date of birth'), null=True, blank=True)
    address = models.TextField(_('Address'), null=True, blank=True)
    zip_code = models.CharField(_('Zip code'), max_length=50, null=True,
            blank=True)
    town = models.CharField(_('Town'), max_length=255, null=True, blank=True)
    country = models.CharField(_('Country'), max_length=255, null=True,
            blank=True)
    mobile_phone = models.CharField(_('Mobile phone'), max_length=50, null=True,
            blank=True)
    landline = models.CharField(_('Landline'), max_length=50, null=True,
            blank=True)
    external_email = models.EmailField(_('External email'), null=True,
            blank=True)
    ast = models.BooleanField(_('Admitted under'), default=False)
    default_picture = models.ImageField(_('Default picture'), upload_to='junk',
            null=True, blank=True)
    picture = models.ImageField(_('Picture'), upload_to='pictures/custom',
            null=True, blank=True)
    valid_picture = models.BooleanField(_('Valid picture'), default=False)

    CORRIDOR = (
            ('1A', '1A'),
    )
    room = models.CharField(_('Room'), max_length=50, null=True)
    corridor = models.CharField(_('Corridor'), choices=CORRIDOR,
            max_length=50, null=True)

    # Network
    site = models.URLField(_('Blog/Website'), verify_exists=False, null=True)
    linkedin = models.URLField(_('Linkedin profile'), verify_exists=False,
            null=True)
    facebook = models.URLField(_('Facebook profile'), verify_exists=False,
            null=True)
    twitter = models.URLField(_('Twitter profile'), verify_exists=False,
            null=True)
    openid = models.URLField(_('OpenID URL'), verify_exists=False, null=True)
    msn = models.EmailField(_('MSN'), null=True)

    AXE_1 = (
            ('ISI', 'ISI'),
    )
    AXE_2 = (
            ('Instrumentation', 'Instrumentation'),
    )
    AXE_3 = (
            ('Éléments finis', 'Éléments finis'),
    )
    OPTION = (
            ('Info', 'Info'),
    )
    generic_axis_1 = models.CharField(_('1st generic axis'), max_length=255,
            choices=AXE_1, null=True)
    generic_axis_2 = models.CharField(_('2nd generic axis'), max_length=255,
            choices=AXE_2, null=True)
    generic_axis_3 = models.CharField(_('3rd generic axis'), max_length=255,
            choices=AXE_3, null=True)
    option = models.CharField(_('Option'), max_length=255,
            choices=OPTION, null=True)

    # Internships, placements
    stage_1a = models.TextField(_('1st year internship'), null=True)
    type_stage_1a = models.CharField(_('Type'), max_length=255, null=True)
    stage_2a = models.TextField(_('2nd year internship'), null=True)
    type_stage_2a = models.CharField(_('Type'), max_length=255, null=True)
    stage_3a = models.TextField(_('3rd year internship'), null=True)
    type_stage_3a = models.CharField(_('Type'), max_length=255, null=True)

    # Other stuff
    sejours = models.CharField(_('Abroad trips'), max_length=255, null=True)
    clubs = models.CharField(_('Clubs'), max_length=255, null=True)
    leisure = models.CharField(_('Leisure activities'), max_length=255,
            null=True)
    leisure_other = models.TextField(_('Other'), null=True)

    def __unicode__(self):
        return u'Profile for %s' % self.user

    @property
    def current_picture(self):
        if self.valid_picture:
            return self.picture
        else:
            return self.default_picture


# Signal handler
# Creates a profile if a user has just been created

def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = UserProfile.objects.create(user=instance,
                promo=datetime.now().year)
        profile.default_picture = 'pictures/promo%s/%s.jpg' % (profile.promo,
                profile.user.username)
        profile.save()

models.signals.post_save.connect(create_profile, User)
