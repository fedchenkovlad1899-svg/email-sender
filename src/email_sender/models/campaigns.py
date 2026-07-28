from django.conf import settings
from django.db import models
from .contacts import Contact
from .message_templates import MessageTemplate
from .contact_groups import ContactGroup
from django.utils import timezone


class Campaign(models.Model):
    """
    Рассылка
    """
    class SendingStatus(models.TextChoices):
        DRAFT = "draft", "Черновик"
        SCHEDULED = "scheduled", "Запланирована"
        PROCESSING  = "processing", "Отправляется"
        COMPLETED  = "completed", "Завершена"
        COMPLETED_WITH_ERRORS = "completed_with_errors", "Завершена c ошибками"
        FAILED = "failed", "Ошибка"
        CANCELED = "canceled", "Отменена"

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
        blank=True,
        related_name="campaigns",
        verbose_name="Контакты",
    )
    contact_group = models.ForeignKey(
        ContactGroup,
        on_delete=models.SET_NULL,   #чтобы осталась история рассылки ,если удалят группу контактов
        null=True,
        blank=True,
        related_name="campaigns",
        verbose_name="Группа контактов",
    )
    status = models.CharField(
        max_length=25,
        choices=SendingStatus.choices,
        default=SendingStatus.DRAFT,
        verbose_name="Статус",
    )

    total_count = models.PositiveIntegerField(default=0,verbose_name="Всего получателей")  #cтатистика получателей
    sent_count = models.PositiveIntegerField(default=0,verbose_name="Отправлено ")
    failed_count = models.PositiveIntegerField(default=0,verbose_name="Ошибок")
    sent_at = models.DateTimeField(null=True,blank=True,verbose_name="Дата отправки")
    scheduled_at = models.DateTimeField(null=True,blank=True,verbose_name="Дата запланированной отправки")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"


    def update_statistics(
            self,
            total: int,
            sent: int,
            failed: int
    )-> None    :
        """
        Обновление статистики после отправки рассылки
        """
        self.total_count = total
        self.sent_count = sent
        self.failed_count = failed
        self.sent_at = timezone.now()

        if total == 0 or sent == 0 :
            self.status = self.SendingStatus.FAILED
        elif failed == 0:
            self.status = self.SendingStatus.COMPLETED
        else:
            self.status = self.SendingStatus.COMPLETED_WITH_ERRORS


    def __str__(self)-> str:
        return self.title