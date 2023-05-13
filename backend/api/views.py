from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from djoser.views import UserViewSet
from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from recipes.models import Ingredient, Recipe, Tag

from .paginator import PageNumberPaginator
from .permissions import IsAdmin, IsAuthorOrReadOnlyPermission
from .serializers import (CustomUserSerializer, IngredientSerializer,
                          RecipeSerializer, TagSerializer)


class ReciepViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAdmin | IsAuthorOrReadOnlyPermission)

    def create(self, serializer):
        serializer.save(author=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPaginator
    add_serializer = CustomUserSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    permission_classes = (IsAdmin | IsAuthorOrReadOnlyPermission)
    serializer_class = IngredientSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    permission_classes = (IsAdmin | IsAuthorOrReadOnlyPermission)
    serializer_class = TagSerializer
