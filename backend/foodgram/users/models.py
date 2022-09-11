from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser, UserManager


class User(AbstractUser):
    username = models.CharField(
        verbose_name='Никнейм пользователя',
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
        verbose_name='Электронная почта',
        unique=True,
        max_length=254
    )
    first_name = models.CharField(
        verbose_name='Имя пользователя',
        max_length=50,
    )
    last_name = models.CharField(
        verbose_name='Фамилия пользователя',
        max_length=50,
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    EMAIL_FIELD = 'email'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='follower'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='following'
    )

    def __str__(self):
        return f'{self.user} подписан на {self.author}'

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'

        constraints = (
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='follow_user_author_constraint'
            ),
        )