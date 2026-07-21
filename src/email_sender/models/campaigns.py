from django.conf import settings
from django.db import models
from .contacts import Contact
from .message_templates import MessageTemplate


class Campaign(models.Model):
    """
    Рассылка
    """
    class SendingStatus(models.TextChoices):
        DRAFT = "draft", "Черновик"
        SCHEDULED = "scheduled", "Запланирована"
        SENDING = "sending", "Отправляется"
        SENT = "sent", "Завершена"
        FAILED = "failed", "Ошибка"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="campaigns",
        verbose_name="Владелец",
    )
    title = models.CharField(
        max_length=255,
        verbose_name="Название",
    )
    template = models.ForeignKey(
        MessageTemplate,
        on_delete=models.PROTECT,   #не удалить,пока используется в какойто рассылке
        related_name="campaigns",
        verbose_name="Шаблон",
    )
    contacts = models.ManyToManyField(
        Contact,
        related_name="campaigns",
        verbose_name="Контакты",
    )
    status = models.CharField(
        max_length=20,
        choices=SendingStatus.choices,
        default=SendingStatus.DRAFT,
        verbose_name="Статус",
    )
    scheduled_at = models.DateTimeField(verbose_name="Дата отправки")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"

    def __str__(self):
        return self.title