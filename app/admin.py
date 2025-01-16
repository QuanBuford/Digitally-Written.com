from django.contrib import admin
from .models import Post

# Define a custom admin class for the Post model
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    list_filter = ('created_at', 'author')

# Ensure Post is registered only once
admin.site.register(Post, PostAdmin)
