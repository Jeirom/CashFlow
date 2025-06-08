from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    first_name = models.CharField(
        max_length=30, blank=True, null=True, verbose_name="Имя"
    )
    last_name = models.CharField(
        max_length=30, blank=True, null=True, verbose_name="Фамилия"
    )

    email = models.EmailField(
        unique=True,
        verbose_name="Email",
    )

    phone = models.CharField(
        max_length=11,
        blank=True,
        null=True,
        verbose_name="Номер телефона",
    )
    token = models.CharField(
        max_length=150, verbose_name="Токен", blank=True, null=True
    )
    is_active = models.BooleanField(blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
