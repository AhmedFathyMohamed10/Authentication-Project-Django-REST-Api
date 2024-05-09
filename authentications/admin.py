from django.contrib import admin
from .models import *

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user',)
    list_filter = ('user',)
    search_fields = ('user',)

admin.site.register(UserProfile, ProfileAdmin)