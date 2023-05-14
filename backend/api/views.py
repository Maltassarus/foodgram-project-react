from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from djoser.views import UserViewSet
from recipes.models import Ingredient, Recipe, Tag
from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import IsAuthenticated

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
    serializer_class = UserAdminSerializer
    queryset = User.objects.all()
    permission_classes = (IsAdminOrSuperuser,)
    pagination_class = LimitOffsetPagination
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=(IsAuthenticated,),
        serializer_class=UserSerializer,
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data, status.HTTP_200_OK)
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)


class SignUpViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class = SignUpSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    http_method_names = ['post']

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if self.is_user_not_existing(request):
            serializer.is_valid(raise_exception=True)
        else:
            serializer.is_valid()
        headers = self.get_success_headers(serializer.data)
        response = Response(
            serializer.data,
            status=status.HTTP_200_OK,
            headers=headers,
        )
        user, _ = User.objects.get_or_create(**response.data)
        self.send_confirmation_code(user)
        return response

    def send_confirmation_code(self, user):
        subject = 'Confirmation of registration'
        code = default_token_generator.make_token(user)
        message = f'confirmation_code : "{code}"'
        recipient_list = [user.email]
        send_mail(
            subject=subject,
            message=message,
            from_email=None,
            recipient_list=recipient_list,
        )

    def is_user_not_existing(self, request):
        return not (
            User.objects
            .filter(username=request.data.get('username', ''))
            .filter(email=request.data.get('email', ''))
            .exists()
        )


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    permission_classes = (IsAdmin | IsAuthorOrReadOnlyPermission)
    serializer_class = IngredientSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    permission_classes = (IsAdmin | IsAuthorOrReadOnlyPermission)
    serializer_class = TagSerializer
