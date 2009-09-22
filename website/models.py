from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class ArticleManager(models.Manager):
    def private(self):
        # Public AND private articles
        return Article.objects.filter(status__in=['public', 'private'])

    def public(self):
        # Only public articles
        return Article.objects.filter(status='public')


class Article(models.Model):
    STATUS_CHOICES = (
            ('draft', _('Draft')),
            ('public', _('Public')),
            ('private', _('Private')),
    )

    TEXTILE = _('''<a href="http://hobix.com/textile/">Textile</a> syntax''')

    title = models.CharField(_('Title'), max_length=200)
    slug = models.SlugField(_('Slug'), max_length=200, unique=True)
    author = models.ForeignKey(User)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    content = models.TextField(_('Content'), help_text=TEXTILE)
    creation_date = models.DateTimeField(_('Creation date'), auto_now_add=True)
    modification_date = models.DateTimeField(_('Publication date'), auto_now=True)

    objects = ArticleManager()

    class Meta:
        ordering = ('-creation_date',)

    def __unicode__(self):
        return u'%s' % self.title

    @models.permalink
    def get_absolute_url(self):
        return ('article', (), {'slug': self.slug})


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        exclude = ('slug', 'author', 'status',)
