from django.contrib.auth.tokens import default_token_generator
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from djoser.views import UserViewSet
from rest_framework import filters, mixins, viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.response import Response

from django.contrib.auth import get_user_model
from recipes.models import Ingredient, Recipe, Tag
from .paginator import PageNumberPaginator
from .permissions import IsAdmin, IsAuthorOrReadOnlyPermission
from .serializers import (CustomUserSerializer, IngredientSerializer,
                          RecipeSerializer, TagSerializer, SignUpSerializer,
                          TokenSerializer)

User = get_user_model()


@api_view(['post'])
@permission_classes([AllowAny])
def token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data['username'],
    )

    if not default_token_generator.check_token(
        user,
        serializer.validated_data['confirmation_code']
    ):
        error_message = 'Неверный confirmation_code'
        return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

    jwt = AccessToken.for_user(user)
    return Response({'token': str(jwt)}, status=status.HTTP_200_OK)


class ReciepViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAdmin | IsAuthorOrReadOnlyPermission)

    def create(self, serializer):
        serializer.save(author=self.request.user)


class CustomUserViewSet(UserViewSet):
    serializer_class = CustomUserSerializer
    queryset = User.objects.all()
    pagination_class = PageNumberPaginator
    permission_classes = (IsCurrentUserOrAdminOrReadOnly,)
    
    @action(
        detail=False,
        permission_classes=[IsAuthenticated],
        methods=['post'],
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
