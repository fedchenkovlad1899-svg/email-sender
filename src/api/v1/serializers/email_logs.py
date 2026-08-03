from rest_framework import serializers
from email_sender.models import EmailLog


class EmailLogSerializer(serializers.ModelSerializer):
    """
    Логи отправки писем
    """
    campaign_title = serializers.CharField(source="campaign.title",read_only=True)
    contact_email = serializers.EmailField(source="contact.email",read_only=True)

    class Meta:
        model = EmailLog
        fields = (
            "id",
            "campaign",
            "campaign_title",
            "contact",
            "contact_email",
            "status",
            "error_message",
            "sent_at",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "campaign",
            "campaign_title",
            "contact",
            "contact_email",
            "status",
            "error_message",
            "sent_at",
            "created_at",
            "updated_at",
        )