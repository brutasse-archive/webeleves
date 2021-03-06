from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from datetime import datetime

from website.models import Article, Event

class ArticleTest(TestCase):
    def test_article(self):
        user = User.objects.create_user('testuser', 'bob@example.com', 'pass')
        article = Article(title='My article', slug='my-article', author=user,
                status='private', content='Well, nothing interesting')
        article.save()

        from_db = Article.objects.get(pk=article.id)

        # __unicode__
        self.assertEquals('My article', '%s' % from_db)

        # get_absolute_url()
        self.assertTrue(from_db.slug in from_db.get_absolute_url())

        # private()
        self.assertTrue(from_db.private)

class EventTest(TestCase):
    def test_event(self):
        user = User.objects.create_user('testuser', 'bob@example.com', 'pass')
        event = Event(title='Party', date=datetime.now(), place='Place',
                user=user)

        # __unicode__
        self.assertEquals('%s' % event, 'Party')

class WebsiteTest(TestCase):
    def test_homepage(self):
        response = self.client.get(reverse('home'))
        self.assertEquals(response.status_code, 200)
        self.assertTrue('Accueil' in response.content)

    def test_article(self):
        """Behaviour of the Article model"""
        # Create a user
        user = User.objects.create_user('testuser', 'bob@example.com', 'pass')

        article = Article(title='Testing', slug='testing', author=user,
                status='private', content='This is a test article')
        article.save()
        
        # This is not viewable by an anonymous user
        url = reverse('article', args=[article.slug])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

        # If the user is logged in, he can read it
        self.client.login(username='testuser', password='pass')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTrue('This is a test article' in response.content)

    def test_login_failure(self):
        url = reverse('login')
        data = {'username': 'test', 'password': 'test'}
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertTrue('errorlist' in response.content)
