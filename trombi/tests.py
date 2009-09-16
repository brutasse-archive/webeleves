from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

class TrombiTest(TestCase):
    def setUp(self):
        """Add a user and his profile"""
        self.user = User.objects.create_user('testuser', 'test@example.com',
                'pass')
        self.client.login(username='testuser', password='pass')

    def test_trombi(self):
        """Homepage of the trombi app"""
        response = self.client.get(reverse('trombi:trombi'))
        self.assertEquals(response.status_code, 200)
        self.assertTrue('Trombinoscope' in response.content)

    def test_profile(self):
        """Profile of the logged in user"""
        response = self.client.get(reverse('trombi:profile'))
        self.assertEquals(response.status_code, 200)
        self.assertTrue('Profile' in response.content)

    def test_edit_profile(self):
        url = reverse('trombi:edit_profile')
        # GET the form
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTrue('Edit your profile' in response.content)
