from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (IngredientViewSet, ReciepViewSet,
                    TagViewSet, UserViewSet)

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
