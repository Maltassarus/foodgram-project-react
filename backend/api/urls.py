from django.urls import include, path, re_path
from rest_framework import routers
from rest_framework.routers import SimpleRouter

from .views import (IngredientViewSet, ReciepViewSet, SignUpViewSet,
                    TagViewSet, UserViewSet, token)

app_name = 'api'

router = SimpleRouter()
router.register('users', UserViewSet, 'users')
router.register('recipes', ReciepViewSet, 'recipes')
router.register('tags', TagViewSet, 'tags')
router.register('ingredients', IngredientViewSet, 'ingredients')

urlpatterns = (
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls')),
    path('', include(router.urls)),
)
