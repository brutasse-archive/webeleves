from django.contrib import admin

from trombi.models import UserProfile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'promo')

admin.site.register(UserProfile, ProfileAdmin)
