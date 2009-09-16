# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.conf import settings

import ldap

class LDAPBackend(object):
    """A simple LDAP authentication backend"""
    def authenticate(self, username=None, password=None):
        if not self.is_valid(username, password):
            return None

        return user.objects.get(username=username)

    def is_valid(self, username, password):
        if password is None or password == '':
            return False

        binddn = '%s@%s' % (username, settings.LDAP_DOMAIN) # emse.fr / messel.emse.fr
        try:
            l = ldap.initialize(settings.LDAP_SERVER) # ldap://localhost
            l.simple_bind_s(binddn, password)
            l.unbind_s()
            return True
        except ldap.LDAPError:
            return False


    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
