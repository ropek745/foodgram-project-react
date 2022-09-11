from django.contrib import admin

from .models import (
    AmountIngredient,
    Favorite,
    Ingredient,
    Recipe,
    ShoppingCart,
    Tag
)


class RecipeIngredientsAdmin(admin.StackedInline):
    model = AmountIngredient
    autocomplete_fields = ('ingredients',)


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'text', 'cooking_time', 'pub_date', 'get_favorite_count'
    )
    search_fields = (
        'name', 'cooking_time',
        'author__username', 'ingredients__name'
    )
    list_filter = ('pub_date', 'tags',)


class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('id', 'user',)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit',)
    search_fields = ('name',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug',)
    search_fields = ('name', 'slug',)


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')


admin.site.register(Recipe)
admin.site.register(ShoppingCart)
admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(Favorite)
