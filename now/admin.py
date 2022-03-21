from django.contrib import admin

from .models import *


class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'email',
        'bio',
        'photo',
        'location',
        'date_joined'
    )
    list_display_links = (
        'id',
        'username'
    )
    search_fields = (
        'username',
        'bio',
        'location'
    )
    list_editable = (
        'location',
    )
    list_filter = (
        'location',
        'date_joined'
    )
    prepopulated_fields = {
        'slug': ('username',)
    }


class EventAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'time_create',
        'time_update',
        'photo',
        'is_published'
    )
    list_display_links = (
        'id',
        'title'
    )
    search_fields = (
        'title',
        'content'
    )
    list_editable = (
        'is_published',
    )
    list_filter = (
        'is_published',
        'time_update'
    )
    prepopulated_fields = {
        'slug': ('title',)
    }


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'category_name'
    )
    list_display_links = (
        'id',
        'category_name'
    )
    search_fields = (
        'category_name',
    )
    prepopulated_fields = {
        'slug': ('category_name',)
    }


class UserJoinEventAdmin(admin.ModelAdmin):
    list_display = (
        'event',
        'user'
    )
    list_display_links = (
        'event',
        'user'
    )
    search_fields = (
        'event',
        'user'
    )
    list_filter = (
        'event',
        'user'
    )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(UserJoinEvent, UserJoinEventAdmin)
admin.site.site_title = 'Админ-панель NOW'
admin.site.site_header = 'Админ-панель NOW'
