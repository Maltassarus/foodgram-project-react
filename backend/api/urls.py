from django.urls import include, path, re_path
from rest_framework import routers
from rest_framework.routers import SimpleRouter

from .views import (IngredientViewSet, ReciepViewSet, SignUpViewSet,
                    TagViewSet, UserViewSet, token)

app_name = 'api'

router = SimpleRouter()
router.register('auth/signup', SignUpViewSet, 'signup')
router.register('users', UserViewSet, 'users')
router.register('recipes', ReciepViewSet, 'recipes')
router.register('tags', TagViewSet, 'tags')
router.register('ingredients', IngredientViewSet, 'ingredients')

urlpatterns = (
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path(r'/', include('djoser.urls')),
    path("", include(router.urls)),
)
