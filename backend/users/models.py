from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


class User(AbstractUser):

    ROLES = (
        ('user', 'Пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор')
    )

    username = models.CharField(
        'Уникальный юзернейм',
        max_length=150,
        unique=True,
        validators=[UnicodeUsernameValidator()],
        error_messages={
            'unique': 'Пользователь с таким именем существует.',
        },
    )
    password = models.CharField(
        'Пароль',
        max_length=150,
    )
    email = models.CharField(
        'Адрес электронной почты',
        max_length=254,
        unique=True,
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
    )

    @property
    def is_admin(self):
        return self.role == self.ROLES[2]

    @property
    def is_moderator(self):
        return self.role == self.ROLES[1]

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email',
            )
        ]


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        related_name='user',
        verbose_name='Подписчик',
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        related_name='author',
        verbose_name='Автор',
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='subscribe_link',
            )
        ]
