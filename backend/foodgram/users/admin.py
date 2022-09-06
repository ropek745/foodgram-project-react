from django.contrib import admin

from .models import User
from food.models import Tag, Ingredient


class UserAdmin(admin.ModelAdmin):
    list_display = ('username',
                    'email',
                    'first_name',
                    'last_name'
                    )


admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Ingredient)