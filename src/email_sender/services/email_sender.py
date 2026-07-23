from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from email_sender.models import Campaign, EmailLog


def send_campaign(campaign):
    """
    Отправляет письма всем получателям выбранной рассылки
    Получатели могут быть выбраны:
    1. Из группы контактов
    2. По одному через поле contacts
    3. Одновременно из группы и вручную
    """

    # разрешенные статусы для запуска рассылки
    allowed_statuses = [
        Campaign.SendingStatus.DRAFT,
        Campaign.SendingStatus.SCHEDULED,
        Campaign.SendingStatus.FAILED,
    ]

    if campaign.status not in allowed_statuses:
        raise ValueError(f'Рассылку со статусом "{campaign.get_status_display()}"нельзя запустить')

    # set чтобы не дублировались контакты
    recipients = set()

    # добавляем контакты из групп
    if campaign.contact_group:
        for contact in campaign.contact_group.contacts.all():
            recipients.add(contact)

    # добавляем контакты по 1
    for contact in campaign.contacts.all():
        recipients.add(contact)

    # количество получателей
    total_count = len(recipients)

    # устанавливаем статус PROCESSING чтобы было понятно что процесс запущен
    campaign.status = Campaign.SendingStatus.PROCESSING
    campaign.total_count = total_count
    campaign.sent_count = 0
    campaign.failed_count = 0
    campaign.sent_at = None

    campaign.save(
        update_fields=[
            "status",
            "total_count",
            "sent_count",
            "failed_count",
            "sent_at",
            "updated_at",
        ]
    )

    # если получателей нет-ничего не отправляем
    if total_count == 0:
        campaign.update_statistics(
            total=0,
            sent=0,
            failed=0,
        )
        campaign.save(
            update_fields=[
                "status",
                "total_count",
                "sent_count",
                "failed_count",
                "sent_at",
                "updated_at",
            ]
        )
        return {
            "total": 0,
            "sent": 0,
            "failed": 0,
        }

    #  шаблон письма
    template = campaign.template

    # cчётчики отправок
    sent_count = 0
    failed_count = 0

    # отправляем письмо каждому контакту
    for contact in recipients:
        log_status = EmailLog.Status.SENT
        error_message = ""
        email_sent_at = None

        try:
            send_mail(
                subject=template.subject,
                message=template.body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[contact.email],
                fail_silently=False,
            )
            sent_count += 1
            email_sent_at = timezone.now()

        except Exception as error:
            log_status = EmailLog.Status.FAILED
            error_message = str(error)
            failed_count += 1

        # создаём лог для каждого контакта
        EmailLog.objects.create(
            campaign=campaign,
            contact=contact,
            status=log_status,
            error_message=error_message,
            sent_at=email_sent_at,
        )

    # обновляем статистику рассылки
    campaign.update_statistics(
        total=total_count,
        sent=sent_count,
        failed=failed_count,
    )
    campaign.save(
        update_fields=[
            "status",
            "total_count",
            "sent_count",
            "failed_count",
            "sent_at",
            "updated_at",
        ]
    )

    # результат возвращается в виде словаря
    return {
        "total": total_count,
        "sent": sent_count,
        "failed": failed_count,
    }