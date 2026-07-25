from django.contrib import admin, messages
from email_sender.services import send_campaign
from email_sender.models import (
    Contact,
    MessageTemplate,
    ContactGroup,
    Campaign,
    EmailLog,
)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "email",
        "owner",
        "created_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    search_fields = (
        "name",
        "email",
        "owner__email",
        "owner__username",
    )
    list_filter = ("owner",)
    ordering = (
        "-created_at",
    )

@admin.register(MessageTemplate)
class MessageTemplateAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "subject",
        "owner",
        "created_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    search_fields = (
        "title",
        "subject",
        "owner__email",
        "owner__username",
    )
    list_filter = ( "created_at",)
    ordering = (
        "-created_at",
    )




@admin.register(ContactGroup)
class ContactGroupAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "owner",
        "created_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    search_fields = (
        "title",
        "owner__email",
        "owner__username",
    )
    filter_horizontal = ("contacts",)#для админки.2 колонки для вкл в список
    ordering = (
        "-created_at",
    )



@admin.action(description="Запустить выбранные рассылки")
def send_selected_campaigns(modeladmin, request, queryset):
    """
    Запуск выбранных чз админкурассылок
    """
    successful_campaigns = 0
    skipped_campaigns = 0
    total_sent = 0
    total_failed = 0

    for campaign in queryset:
        try:
            result = send_campaign(campaign)
            successful_campaigns += 1
            total_sent += result["sent"]
            total_failed += result["failed"]

        except ValueError as error:
            skipped_campaigns += 1
            modeladmin.message_user(request,f'Рассылка "{campaign.title}" пропущена: {error}',level=messages.WARNING)

        except Exception as error:
            skipped_campaigns += 1
            campaign.status = Campaign.SendingStatus.FAILED  # если упала ошибка до завершения сервиса
            campaign.save(
                update_fields=[
                    "status",
                    "updated_at",
                ]
            )
            modeladmin.message_user(request,f'Не удалось запустить рассылку "{campaign.title}": {error}',level=messages.ERROR)

    if successful_campaigns > 0 :
        modeladmin.message_user(
            request,
            (
                f"Обработано рассылок:{successful_campaigns}  "
                f"Отправлено писем:{total_sent}  "
                f"Ошибок отправки:{total_failed}  "
            ),
            level=messages.SUCCESS
        )

    if skipped_campaigns:
        modeladmin.message_user(request,f"Пропущено рассылок: {skipped_campaigns}",level=messages.WARNING)





@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "owner",
        "status",
        "total_count",
        "sent_count",
        "failed_count",
        "scheduled_at",
        "sent_at",
        "created_at",
    )
    readonly_fields = (
        "status",
        "total_count",
        "sent_count",
        "failed_count",
        "sent_at",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "status",
        "scheduled_at",
        "sent_at",
        "created_at",
    )
    search_fields = (
        "title",
        "owner__email",
        "owner__username",
        "template__subject",
    )
    filter_horizontal = ("contacts",)
    autocomplete_fields = (
        "owner",
        "template",
        "contact_group",
    )
    actions = (
        send_selected_campaigns,
    )
    ordering = (
        "-created_at",
    )
    fieldsets = (
        (
            "Основная информация",
            {
                "fields": (
                    "owner",
                    "title",
                    "template",
                ),
            },
        ),
        (
            "Получатели",
            {
                "fields": (
                    "contact_group",
                    "contacts",
                ),
            },
        ),
        (
            "Планирование",
            {
                "fields": (
                    "scheduled_at",
                ),
            },
        ),
        (
            "Результат отправки",
            {
                "fields": (
                    "status",
                    "total_count",
                    "sent_count",
                    "failed_count",
                    "sent_at",
                ),
            },
        ),
        (
            "Системная информация",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
                "classes": (
                    "collapse",
                ),
            },
        ),
    )


    def save_model(self, request, obj, form, change):
        """
        для смены статуса c DRAFT на SCHEDULED при добавлении чз админку
        """

        if (obj.status == Campaign.SendingStatus.DRAFT and obj.scheduled_at):
            obj.status = Campaign.SendingStatus.SCHEDULED
        super().save_model(
            request,
            obj,
            form,
            change,
        )







@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "campaign",
        "contact",
        "status",
        "sent_at",
        "created_at",
    )
    readonly_fields = (
        "campaign",
        "contact",
        "status",
        "error_message",
        "sent_at",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "status",
        "sent_at",
        "created_at",
    )
    search_fields = (
        "contact__email",
        "campaign__title",
        "campaign__owner__email",
        "campaign__owner__username",
    )
    ordering = (
        "-created_at",
    )




    def has_add_permission(self, request):
        """
        Запрещает создавать логи
        """
        return False

    def has_view_permission(self, request, obj=None):
        """
        Разрешает просматривать логи
        """
        return True

    def has_change_permission(self, request, obj=None):
        """
        Запрещает изменять логи
        """
        return False

    def has_delete_permission(self, request, obj=None):
        """
        Запрещает удалять историю логи
        """
        return False