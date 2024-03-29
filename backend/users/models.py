from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


class User(AbstractUser):

    ROLES = (
        ('USER', 'Пользователь'),
        ('ADMIN', 'Администратор')
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
    role = models.CharField(
        'Роль',
        max_length=15,
        default=ROLES[1],
    )

    @property
    def is_admin(self):
        return self.role == self.ROLES[1]


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
