from rest_framework import serializers
from email_sender.models import MessageTemplate


class MessageTemplateSerializer(serializers.ModelSerializer):
    """
     шаблоны писем
    """
    class Meta:
        model = MessageTemplate
        fields = (
            "id",
            "title",
            "subject",
            "body",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )

