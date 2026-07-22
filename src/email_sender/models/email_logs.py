from django.db import models
from .campaigns import Campaign
from .contacts import Contact


class EmailLog(models.Model):
    """
    Логи отправки писем
    """
    class Status(models.TextChoices):
        PENDING = "pending", "Ожидает отправки"
        SENT = "sent", "Отправлено"
        FAILED = "failed", "Ошибка"

    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.CASCADE,
        related_name="email_logs",
        verbose_name="Рассылка",
    )
    contact = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE,
        related_name="email_logs",
        verbose_name="Контакт",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name="Статус",
    )
    error_message = models.TextField(
        blank=True,
        verbose_name="Текст ошибки",
    )
    sent_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Дата отправки",
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
        verbose_name = "История отправки"
        verbose_name_plural = "Истории отправки"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.contact.email} - {self.status}"