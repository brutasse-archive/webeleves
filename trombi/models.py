# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from datetime import datetime
import os

class UserProfile(models.Model):
    # Mandatory fields
    user = models.OneToOneField(User, verbose_name=_('User'))
    promo = models.PositiveIntegerField(_('Promotion'))

    # Not required fields
    bio = models.CharField(_('Titre'), max_length=255, null=True, blank=True,
            help_text='Le titre que vous voulez donner à votre profil')
    surname = models.CharField(_('Surnom'), max_length=255, null=True,
            blank=True)
    date_of_birth = models.DateField(_('Date de naissance'), null=True,
            blank=True, help_text='Format: JJ/MM/AAAA')
    address = models.TextField(_('Adresse'), null=True, blank=True)
    zip_code = models.CharField(_('Code postal'), max_length=50, null=True,
            blank=True)
    town = models.CharField(_('Ville'), max_length=255, null=True, blank=True)
    country = models.CharField(_('Pays'), max_length=255, null=True,
            blank=True, default='France')
    mobile_phone = models.CharField(_('Portable'), max_length=50, null=True,
            blank=True)
    landline = models.CharField(_('Fixe'), max_length=50, null=True,
            blank=True)
    external_email = models.EmailField(_('Email (non ecole)'), null=True,
            blank=True)
    ast = models.BooleanField(_('AST'), default=False)
    default_picture = models.ImageField(_('Default picture'), upload_to='junk',
            null=True, blank=True)
    picture = models.ImageField(_('Photo'), upload_to='pictures/custom',
            null=True, blank=True)
    valid_picture = models.BooleanField(_('Photo valide'), default=False)

    CORRIDOR = (
            ('0D', '0D'),
            ('1A', '1A'),
            ('1B', '1B'),
            ('1C', '1C'),
            ('1D', '1D'),
            ('2A', '2A'),
            ('2B', '2B'),
            ('2C', '2C'),
            ('2D', '2D'),
            ('3A', '3A'),
            ('3B', '3B'),
            ('3C', '3C'),
            ('3D', '3D'),
            ('4A', '4A'),
            ('4B', '4B'),
            ('4C', '4C'),
            ('4D', '4D'),
            ('5A', '5A'),
            ('5B', '5B'),
            ('5C', '5C'),
            ('5D', '5D'),
            ('Cyborg', 'Cyborg'),
            ('1NME', '1NME'),
            ('2NME', '2NME'),
            ('3NME', '3NME'),
            ('4NME', '4NME'),
            ('5NME', '5NME'),
            ('6NME', '6NME'),
            ('7NME', '7NME'),
            ('Hors ME', 'Hors ME'),
    )
    room = models.CharField(_('Chambre'), max_length=50, null=True, blank=True)
    corridor = models.CharField(_('Couloir'), choices=CORRIDOR,
            max_length=50, null=True)

    def me(self):
        return self.corridor != 'Hors ME' and self.corridor is not None

    # Network
    site = models.URLField(_('Blog/Website'), verify_exists=False, null=True,
            blank=True)
    linkedin = models.URLField(_('Linkedin profile'), verify_exists=False,
            null=True, blank=True)
    facebook = models.URLField(_('Facebook profile'), verify_exists=False,
            null=True, blank=True)
    twitter = models.URLField(_('Twitter profile'), verify_exists=False,
            null=True, blank=True)
    openid = models.URLField(_('URL OpenID'), verify_exists=False, null=True,
            blank=True)
    msn = models.EmailField(_('MSN'), null=True, blank=True)

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

    def has_picture(self):
        if self.current_picture:
            return os.path.exists(self.current_picture.path)


# Signal handler
# Creates a profile if a user has just been created

def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = UserProfile.objects.create(user=instance,
                promo=datetime.now().year)
        profile.save()

models.signals.post_save.connect(create_profile, User)
