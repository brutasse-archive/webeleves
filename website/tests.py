from django.test import TestCase
from django.core.urlresolvers import reverse

class WebsiteTest(TestCase):
    def test_homepage(self):
        response = self.client.get(reverse('home'))
        self.assertEquals(response.status_code, 200)
        self.assertTrue('Accueil' in response.content)
