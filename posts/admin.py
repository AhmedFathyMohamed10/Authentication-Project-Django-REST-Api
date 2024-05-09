from django.contrib import admin
from .models import Post
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author')
    search_fields = ('title__icontains', 'content__icontains', 'author__username')
    list_filter = ('author', 'created_at')


admin.site.register(Post, PostAdmin)