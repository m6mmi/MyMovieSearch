from django.contrib import admin

from userprofiles.models import UserProfile, FavoriteMovie

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(FavoriteMovie)