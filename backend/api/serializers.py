from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers, validators
from rest_framework.fields import IntegerField, SerializerMethodField
from rest_framework.relations import SlugRelatedField

from recipes.models import Follow, Ingredient, Recipe, RecipeIngredient, Tag

User = get_user_model()


class SignUpBaseSerializer(serializers.ModelSerializer):

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError(
                'Использовать имя \'me\' в качестве username запрещено.'
            )
        return username


class SignUpSerializer(SignUpBaseSerializer):

    class Meta:
        model = User
        fields = ('email', 'username',)


class RecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    image = Base64ImageField()
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
    )
    ingredients = SerializerMethodField()
    in_shopping_cart = SerializerMethodField(read_only=True)
    is_favorite = SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = '__all__'

    def create(self, validated_data):
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(validated_data.pop('tags'))
        recipe.ingredients.set(validated_data.pop('ingredients'))

    def validate(self, attrs):
        if not len(attrs['ingredients']):
            raise serializers.ValidationError(
                'Пустой список ингредиентов.'
            )
        ingredient_list = []
        for ingredient in attrs['ingredients']:
            if ingredient['name'] in ingredient_list:
                raise serializers.ValidationError(
                    'Ингредиенты не должны повторяться.'
                )
            ingredient_list.append(ingredient['name'])
            if ingredient['amount'] <= 0:
                raise serializers.ValidationError(
                    'Количество ингредиента должно быть больше нуля.'
                )
        if not len(attrs['tags']):
            raise serializers.ValidationError(
                'Пустой список тегов.'
            )
        if attrs['cooking_time'] <= 0:
            raise serializers.ValidationError(
                'Время готовки должно быть больше нуля.'
            )


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'email',
            'first_name',
            'last_name',
        )


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = IntegerField(write_only=True)

    class Meta:
        model = RecipeIngredient
        fields = '__all__'


class SignUpBaseSerializer(serializers.ModelSerializer):

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError(
                'Использовать имя \'me\' в качестве username запрещено.'
            )
        return username


class SignUpSerializer(SignUpBaseSerializer):

    class Meta:
        model = User
        fields = ('email', 'username',)
