from django.urls import include, path
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
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/token/', token, name='token')
)
