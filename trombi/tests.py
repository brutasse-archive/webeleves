# -*- coding: utf-8 -*-
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from trombi.models import UserProfile

class ProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@example.com',
                'pass')

    def test_profile(self):
        profile = self.user.get_profile()
        # __unicode__
        self.assertEquals('Profile for testuser', '%s' % profile)

        profile.default_picture = 'pictures/lol.jpg' # Stock picture
        self.assertEquals(profile.default_picture, profile.current_picture)

        profile.picture = 'uploads/custom.jpg' # Custom picture
        self.assertEquals(profile.default_picture, profile.current_picture)
        profile.valid_picture = True # Been approved by the admins
        self.assertEquals(profile.picture, profile.current_picture)

        self.assertFalse(profile.has_picture()) # The file doesn't exist


class TrombiTest(TestCase):
    def setUp(self):
        """Add a user and his profile"""
        self.user = User.objects.create_user('testuser', 'test@example.com',
                'pass')
        self.client.login(username='testuser', password='pass')
        profile = self.user.get_profile()
        profile.promo = 2007
        profile.save()

    def test_trombi(self):
        """Homepage of the trombi app"""
        response = self.client.get(reverse('trombi:trombi'))
        self.assertEquals(response.status_code, 200)
        self.assertTrue('Trombinoscope' in response.content)

    def test_profile(self):
        """Profile of the logged in user"""
        response = self.client.get(reverse('trombi:profile'))
        self.assertEquals(response.status_code, 200)
        self.assertTrue('Modifier mon profil' in response.content)

    def test_edit_profile(self):
        url = reverse('trombi:edit_profile')
        # GET the form
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTrue('Modifier mon profil' in response.content)

        # POST it
        data = {'bio': 'Salut',
                'surname': 'TrombiTester',
                'date_of_birth': '01/01/1983',
                'corridor': '1A',
                'room': '134',
                'external_email': 'bob@example.com',
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 302)

        profile_url = reverse('trombi:profile')
        self.assertTrue(profile_url in response['Location'])

        # Get the modified profile
        response = self.client.get(profile_url)
        self.assertEquals(response.status_code, 200)
        for item in data.values():
            self.assertTrue(item in response.content)

    def test_profile_networks(self):
        url = reverse('trombi:edit_profile_networks')

        # GET the form
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTrue('Réseaux' in response.content)

        # POST it
        data = {
                'twitter': 'http://twitter.com/lol',
                'linkedin': 'http://linkedin.com/in/lol',
        }
        profile_url = reverse('trombi:profile')
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 302)
        self.assertTrue(profile_url in response['Location'])

        # Check the data appears in the profile
        response = self.client.get(profile_url)
        self.assertEquals(response.status_code, 200)
        for item in data.values():
            self.assertTrue(item in response.content)

    def test_promo(self):
        url = reverse('trombi:promo', args=[2007])
        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)
        self.assertTrue('testuser' in response.content)
        self.assertTrue('1 personne' in response.content)


    def test_eleve(self):
        """Profile page of a single person"""
        # Trying to put the wrong promo will redirect you
        url = reverse('trombi:eleve', args=[2004, 'testuser'])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)
        self.assertTrue('2007' in response['Location'])

        # Let's get the real page now
        url = reverse('trombi:eleve', args=[2007, 'testuser'])

        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTrue('profil' in response.content)

    def test_vcard(self):
        """Downloading a vCard"""
        # try with the wrong promo
        url = reverse('trombi:vcard', args=[2004, 'testuser'])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)

        # Right one now
        url = reverse('trombi:vcard', args=[2007, 'testuser'])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response['content-type'], 'text/x-vcard')

    def test_search(self):
        """Searching for users"""
        url = reverse('trombi:search')
        # There is a default value in the box. The users should not submit
        # this value
        data = {'q': u'Nom, prénom, login, surnom'}
        response = self.client.get(url, data)
        self.assertEquals(response.status_code, 302)

        data = {'q': 'what'}
        response = self.client.get(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertTrue('0 personne' in response.content)

        data = {'q': 'testuser'}
        response = self.client.get(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertTrue('1 personne' in response.content)
        self.assertTrue('testuser' in response.content)

        # We can put several keywords if we want
        data = {'q': 'bob lol'}
        response = self.client.get(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertTrue('0 personne' in response.content)

    def test_opensearch(self):
        """Testing the XML opensearch file generation"""
        url = reverse('trombi:opensearch')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response['Content-Type'], 'text/xml')
        self.assertTrue('/search/?q={searchTerms}' in response.content)
