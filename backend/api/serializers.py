from django.conf import settings
from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from foods.models import Ingredient, Tag, AmountIngredient, Recipe
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator
from users.models import User, Follow


class CreateUserSerializer(UserCreateSerializer):
    """Сериализатор для регистрации пользователей."""
    class Meta:
        model = User
        fields = (
            'email', 'password', 'username', 'first_name', 'last_name',
        )
        extra_kwargs = {'password': {'write_only': True}}


class UserListSerializer(UserSerializer):
    """Сериализатор для управления пользователями."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return Follow.objects.filter(
            user=user, author=obj
        ).exists() if user.is_authenticated else False


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для управления тегами"""
    class Meta:
        model = Tag
        fields = (
            'id', 'name', 'color', 'slug',
        )


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для управления ингридиентами"""
    class Meta:
        model = Ingredient
        fields = (
            'id', 'name', 'measurement_unit',
        )


class IngredientCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления ингредиентов при создании рецепта."""
    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = AmountIngredient
        fields = ('id', 'amount')


class IngredientRecipeReadSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )
    id = serializers.ReadOnlyField(source='ingredient.id')

    class Meta:
        model = AmountIngredient
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для рецептов."""
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    author = UserListSerializer(read_only=True)
    tags = TagSerializer(many=True)
    ingredients = IngredientRecipeReadSerializer(
        many=True,
        source='consists_of'
    )

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time',
        )

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return request.user.favorite.filter(recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        if not request.user.is_in_shopping_card:
            return ValidationError('Нет списка покупок!')
        return request.user.cart.filter(recipe=obj).exists()


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания рецептов."""
    ingredients = IngredientCreateSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    image = Base64ImageField(use_url=True, )
    cooking_time = serializers.IntegerField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'ingredients', 'tags', 'image', 'name', 'text',
            'cooking_time', 'author',
        )
        validators = [UniqueTogetherValidator(
            queryset=Recipe.objects.all(),
            fields=['author', 'recipe'])]

    def validate(self, data):
        ingredients_set = set()
        for ingredient in data['ingredients']:
            ingredients_set.add(ingredient['id'])
            if ingredient['amount'] < 1:
                raise serializers.ValidationError(
                    settings.INGREDIENTS_COUNT_ERROR
                )
        if len(ingredients_set) != len(data['ingredients']):
            raise serializers.ValidationError(
                settings.INGREDIENT_REPETITION_ERROR
            )
        return data

    def create_ingredients(self, recipe, ingredients):
        ingredients_list = [
            AmountIngredient(
                ingredient=get_object_or_404(Ingredient, id=ingredient['id']),
                recipe=recipe,
                amount=ingredient['amount']
            ) for ingredient in ingredients
        ]
        AmountIngredient.objects.bulk_create(ingredients_list)

    def create(self, validated_data):
        """Создание рецепта."""
        tags_data = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        image = validated_data.pop('image')
        recipe = Recipe.objects.create(image=image, **validated_data)
        self.create_ingredients(ingredients_data, recipe)
        recipe.tags.set(tags_data)
        return recipe

    def update(self, recipe, validated_data):
        """Редактирование рецепта."""
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        AmountIngredient.objects.filter(recipe=recipe).delete()
        self.create_ingredients(ingredients, recipe)
        recipe.tags.set(tags)
        return super().update(recipe, validated_data)

    def to_representation(self, recipe):
        return RecipeSerializer(
            recipe,
            context={'request': self.context.get('request')}
        ).data


class RecipeSubcribeSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения рецепта в подписке."""
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class SubscribeSerializer(serializers.ModelSerializer):
    """Сериализатор для подписок."""
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField(read_only=True)
    id = serializers.ReadOnlyField(source='author.id')
    email = serializers.ReadOnlyField(source='author.email')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )
        validators = [UniqueTogetherValidator(
            queryset=User.objects.all(),
            fields=['username', 'id'])]

    def get_is_subscribed(self, obj):
        return obj.following.filter(user=obj.user, author=obj.author).exists()
