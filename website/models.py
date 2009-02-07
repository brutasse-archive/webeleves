from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

STATUS_CHOICES = (
        ('draft', _('Draft')),
        ('published', _('Published')),
)

TEXTILE = _('''<a href="http://hobix.com/textile/">Textile</a> syntax''')


class ArticleManager(models.Manager):
    def published(self):
        return Article.objects.filter(status='published').order_by('-creation_date')


class Article(models.Model):
    title = models.CharField(_('Title'), max_length=200)
    slug = models.SlugField(_('Slug'), max_length=200, unique=True)
    author = models.ForeignKey(User)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    content = models.TextField(_('Content'), help_text=TEXTILE)
    creation_date = models.DateTimeField(_('Creation date'), auto_now_add=True)
    modification_date = models.DateTimeField(_('Publication date'), auto_now=True)

    def __unicode__(self):
        return u'%s' % self.title

    objects = ArticleManager()

    @models.permalink
    def get_absolute_url(self):
        return ('article', [str(self.id)])


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        exclude = ('slug', 'author', 'status',)
