from django.contrib import admin
from .models import Post



class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    list_filter = ('created_at', 'author')


admin.site.register(Post, PostAdmin)

# def user_management_view(request):
#     return views.user_management(request)

# admin.site.register_view('user-management/', view=user_management_view, name='user_management')

# def custom_admin_view(request):
#     return HttpResponseRedirect('/admin/')

# admin.site.register_view('custom-view/', view=custom_admin_view, name='custom_view')