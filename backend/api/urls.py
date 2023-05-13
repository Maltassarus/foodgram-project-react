from django.urls import include, path
from rest_framework import routers
from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet, ReciepViewSet, TagViewSet, UserViewSet

app_name = 'api'


router = DefaultRouter()

router.register('recipes', ReciepViewSet, 'recipes')
router.register('users', UserViewSet, 'users')
router.register('tags', TagViewSet, 'tags')
router.register('ingredients', IngredientViewSet, 'ingredients')

urlpatterns = (
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
)
