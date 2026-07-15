from django.db import models
from django.contrib.auth.models import AbstractUser






class User(AbstractUser):
    class Role(models.TextChoices):
        USER = "USER", "Пользователь"
        MANAGER = "MANAGER", "Менеджер"
        ADMIN = "ADMIN", "Администратор"

    role = models.CharField(
        max_length=64,
        choices=Role.choices,
        default=Role.USER,
    )

    def __str__(self):
        return self.username