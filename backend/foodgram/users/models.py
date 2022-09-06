from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(
        'Никнейм пользователя',
        db_index=True,
        unique=True,
        max_length=150,
        validators=[
            RegexValidator(
                regex=r'^[-a-zA-Z0-9_]+$',
                message='Недопустимое имя!'
            )
        ]
    )
    email = models.EmailField(
        'Электронная почта',
        unique=True,
        max_length=254
    )
    first_name = models.CharField(
        'Имя пользователя',
        max_length=50,
        blank=True,
        null=True
    )
    last_name = models.CharField(
        'Фамилия пользователя',
        max_length=50,
        blank=True,
        null=True
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
