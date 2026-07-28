from django.conf import settings
from django.db import models
from .contacts import Contact


class ContactGroup(models.Model):
    """
    Группа контактов
    """
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="contact_groups",
        verbose_name="Владелец",
    )
    title = models.CharField(
        max_length=255,
        verbose_name="Название групп",
    )
    description = models.TextField(
        blank=True,
        verbose_name="Описание",
    )
    contacts = models.ManyToManyField(
        Contact,  #один контакн в нескольких списках может быть
        related_name="contact_groups",
        verbose_name="Контакты",
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления",
    )

    class Meta:
        verbose_name = "Группа  контактов"
        verbose_name_plural = "Группы контактов"
        ordering = ("title",)
        constraints = [
            models.UniqueConstraint(
                fields=("owner", "title"),
                name="unique_contact_group_per_owner",
            ) #пользователь не создаст две обинаковых группы,но другой может созд с таким названием
        ]

    def __str__(self)-> str:
        return self.title