from django.contrib import admin

from .models import (
    AmountIngredient,
    Favorite,
    Ingredient,
    Recipe,
    ShoppingCart,
    Tag
)


@admin.register(AmountIngredient)
class RecipeIngredientsAdmin(admin.ModelAdmin):
    model = AmountIngredient
    search_fields = ['ingredients']


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'text', 'cooking_time', 'pub_date', 'get_favorite_count'
    )
    search_fields = (
        'name', 'cooking_time',
        'author__username', 'ingredients__name'
    )
    list_filter = ('pub_date', 'tags',)

    @admin.display(description='В избранном')
    def get_favorite_count(self, obj):
        return obj.favorite.count()


@admin.register(Favorite)
class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('id', 'user',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit',)
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug',)
    search_fields = ('name', 'slug',)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
