from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from food.models import Ingredient ,Tag
from users.models import User


class CreateUserSerializer(UserCreateSerializer):
    """Сериализатор для регистрации пользователей."""
    class Meta:
        model = User
        fields = (
            'email', 'password', 'username', 'first_name', 'last_name',
        )
        extra_kwargs = {'password': {'write_only': True}}


class GetUserListSerializer(UserSerializer):
    """Сериализатор для управления пользователями."""
    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name'
        )


class GetTagSerializer(serializers.ModelSerializer):
    """Сериализатор для управления тегами"""
    class Meta:
        model = Tag
        fields = (
            'id', 'name', 'color', 'slug'
        )


class GetIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для управления ингридиентами"""
    class Meta:
        model = Ingredient
        fields = (
            'id', 'name', 'measurement_unit'
        )