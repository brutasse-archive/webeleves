# -*- coding: utf-8 -*-
from django.contrib.auth.models import User, Group
from django.core.management.base import BaseCommand
from django.conf import settings

import os
import re
from datetime import datetime

# ldapsearch ou=ICM_1A > dap/1a.txt
# ldapsearch ou=ICM_2A > dap/2a.txt
# ldapsearch ou=ICM_3A > dap/3a.txt

INTERESTING_FIELDS = (
        'sn', # Nom
        'givenName', # Prenom
        'uid', # login
        'mail', # Email
        'ou', # Promo (ICM_?A / promo200?)
)

FIELDS_ASSOC = {
        'sn': 'name',
        'givenName': 'surname',
        'uid': 'login',
        'mail': 'email',
        'ou': 'promo',
}

class LDAPUser(object):
    """A user as parsed from the LDAP directory. Will be stored in the DB"""
    def __init__(self, login, name, surname, email, promo):
        """A bit of cleanup on the parameters"""
        self.login = login
        self.name = name.replace('_', ' ').replace('-', ' ')
        self.surname = surname
        self.email = email
        self.promo = promo.replace('ICM_', '')

    def __repr__(self):
        return '%s: %s %s, %s' % (self.login, self.surname, self.name, self.email)

    def guess_promo(self):
        """self.promo is something like:
         - promo2006
         - promo2005
         - 1A / 2A / 3A
        With a bit of logic we can change it to a year"""
        if self.promo.startswith('promo'):
            return self.promo.replace('promo', '')
        
        study_year = int(self.promo.replace('A', ''))
        this_year = datetime.now().year
        return this_year - study_year + 1

    def to_auth_user(self):
        """Transforms a LDAPUser into a persistent Auth user"""
        user, created = User.objects.get_or_create(username=self.login)
        # Add all the available info
        user.first_name = self.surname
        user.last_name = self.name
        user.email = self.email
        # Only LDAP login please
        user.set_unusable_password()
        user.save()

        if created:
            # A signal created the profile
            profile = user.get_profile()
            profile.promo = self.guess_promo()
            profile.default_picture = 'pictures/promo%s/%s.jpg' % \
                    (profile.promo, profile.user.username)
            profile.save()

        # Cleaning the groups... A user is only part of 1 promo
        try:
            group = Group.objects.get(name=self.promo)
            groups = user.groups.all()
            for g in groups:
                if not g == group:
                    user.groups.remove(g)
            if not group in groups:
                group.user_set.add(user)
        except Group.DoesNotExist:
            # No 1A / 2A / 3A, clean the groups
            for g in user.groups.all():
                user.groups.remove(g)


class LDAPParser(object):
    """Parses a file containing the raw output of an ldapsearch command"""
    def __init__(self, file_name):
        self.file_name = os.path.join(settings.LDAP_DATA, file_name)
        self.users = []

    def read_file(self):
        """Parses the file and fills the self.users list"""
        file = open(self.file_name, 'r')
        for line in file:
            attrs = None
            if not line.startswith('#'):
                attrs = re.search(r'(\w+):\s+(.+)', line)
            if attrs:
                (key, value) = attrs.group(1), attrs.group(2)
                if key in INTERESTING_FIELDS:
                    if FIELDS_ASSOC[key] == 'name':
                        name = value
                    if FIELDS_ASSOC[key] == 'surname':
                        surname = value
                    if FIELDS_ASSOC[key] == 'email':
                        email = value
                    if FIELDS_ASSOC[key] == 'login':
                        login = value
                    if FIELDS_ASSOC[key] == 'promo':
                        promo = value
                        user = LDAPUser(login, name, surname, email, promo)
                        self.users.append(user)
        file.close()

class Command(BaseCommand):
    def handle(self, *args, **options):
        for file in os.listdir(settings.LDAP_DATA):
            parser = LDAPParser(file)
            parser.read_file()
            counter = 0
            for user in parser.users:
                created = user.to_auth_user()
                if created:
                    counter += 1
            print '%s: %s users, %s created' % (user.promo, len(parser.users),
                    counter)
