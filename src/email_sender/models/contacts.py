from django.conf import settings
from django.db import models


class Contact(models.Model):
    """
    Контакт получателя рассылки
    """
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="contacts",
        verbose_name="Владелец"
    )
    name = models.CharField(
        max_length=255,
        verbose_name="Имя"
    )
    email = models.EmailField(
        # unique=True,   чтобы разные польз могли доб одинаковый контакт
        verbose_name="Email"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Описание"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name= "Контакт"
        verbose_name_plural= "Контакты"
        ordering = ["name"]
        #уиникальность почты для каждого пользователя отдельно
        constraints = [
            models.UniqueConstraint(
                fields=["owner", "email"],
                name="unique_contact_email_per_owner",
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.email})"