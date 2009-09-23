# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.conf import settings

import ldap

class LDAPBackend(object):
    """A simple LDAP authentication backend"""
    def authenticate(self, username=None, password=None):
        if not self.is_valid(username, password):
            return None

        return User.objects.get(username=username)

    def is_valid(self, username, password):
        if password is None or password == '':
            return False

        try:
            l = ldap.initialize(settings.LDAP_SERVER) # ldap://localhost
            dn = 'uid=%s,ou=Users,ou=eleves,dc=emse,dc=fr' % username
            l.simple_bind_s(dn, password.encode('utf-8'))
            l.unbind_s()
            return True
        except ldap.LDAPError:
            return False


    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
