from rest_framework import serializers
from email_sender.models import EmailLog


class EmailLogSerializer(serializers.ModelSerializer):
    """
    Логи отправки писем
    """
    class Meta:
        model = EmailLog
        fields = (
            "id",
            "campaign",
            "contacts",
            "status",
            "error_message",
            "sent_at",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "campaign",
            "contacts",
            "status",
            "error_message",
            "sent_at",
            "created_at",
            "updated_at",
        )