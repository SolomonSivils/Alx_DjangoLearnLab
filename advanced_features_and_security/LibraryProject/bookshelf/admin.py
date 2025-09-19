from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UserAdmin
from .models import CustomUser
from django.db import models
from django.conf import settings
from .models import Post 
# Register your models here.
from .models import Book
from django.contrib.auth.models import User

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    search_fields = ('title', 'author')
    list_filter = ('publication_year',)

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'date_of_birth', 'profile_photo')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                   'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password', 'password_confirm', 'date_of_birth', 'profile_photo'),
        }),
    )

admin.site.unregister(User)

admin.site.register(CustomUser, CustomUserAdmin)

class PostAdmin(admin.ModelAdmin):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    # ...
admin.site.register(Post, PostAdmin)  # Register the model with the admin class