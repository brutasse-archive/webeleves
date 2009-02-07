from django.contrib import admin
from website.models import Article

class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-creation_date']
    list_display = ('title', 'author', 'status', 'creation_date', 'modification_date',)
admin.site.register(Article, ArticleAdmin)
