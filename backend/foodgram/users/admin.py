from django.contrib import admin

from .models import User, Follow


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name',)
    search_fields = ('username', 'email',)
    list_filter = ('email', 'first_name',)


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author',)
    search_fields = ('author', 'user',)
    list_filter = ('author',)


admin.site.register(User)
admin.site.register(Follow)