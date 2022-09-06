from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from food.models import Ingredient, Tag
from users.models import User
from .serializers import (
    GetUserListSerializer,
    GetTagSerializer,
    GetIngredientSerializer
)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = GetUserListSerializer
    permission_classes = (AllowAny,)


class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = GetTagSerializer


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = GetIngredientSerializer
