from django.conf import settings
from django.db import models


class MessageTemplate(models.Model):
    """
    Шаблон письма
    """
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name = "message_templates",
        verbose_name = "Пользователь",
    )
    title = models.CharField(max_length = 255,verbose_name ="Название шаблона")
    subject = models.CharField(max_length = 255,verbose_name ="Тема письма")
    body = models.TextField(verbose_name = "Текст письма")
    created_at = models.DateTimeField(auto_now_add = True,verbose_name ="Дата создания")
    updated_at = models.DateTimeField(auto_now = True,verbose_name ="Дата обновления")

    class Meta:
        verbose_name = "Шаблон письма"
        verbose_name_plural = "Шаблоны писем"

        ordering = ["title"]

    def __str__(self)-> str:
        return self.title