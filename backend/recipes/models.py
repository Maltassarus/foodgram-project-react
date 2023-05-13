from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.shortcuts import render

User = get_user_model()


class Ingredient(models.Model):
    id = models.IntegerField(
        'Уникальный id',
        primary_key=True,
    )
    name = models.CharField(
        'Наименование',
        max_length=50,
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=10,
    )

    class Meta:
        verbose_name = 'ingredient'
        verbose_name_plural = 'ingredients'


class Tag(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(
        'Название тега',
        max_length=50
    )
    color = models.CharField(
        'Цвет',
        max_length=7
    )
    slug = models.SlugField()

    class Meta:
        verbose_name = 'tag'
        verbose_name_plural = 'tags'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    ingredients = models.ManyToManyField(Ingredient)
    tags = models.ManyToManyField(Tag)
    image = models.ImageField(
        'Картинка'
    )
    name = models.CharField(
        'Название',
        max_length=200
    )
    text = models.TextField(
        'Описание'
    )
    cooking_time = models.IntegerField(
        'Время приготовления (в минутах)'
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'recipe'
        verbose_name_plural = 'recipes'
        ordering = ['-pub_date']


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite',
    )


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        blank=True,
        null=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'following'], name='follow_link')
        ]


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
    )
    amount = models.IntegerField()


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )
