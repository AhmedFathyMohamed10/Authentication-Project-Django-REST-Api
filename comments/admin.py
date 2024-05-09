from django.contrib import admin
from .models import *

# Register your models here.

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'author', 'post')
    list_filter = ('author', 'post')


admin.site.register(Comment, CommentAdmin)