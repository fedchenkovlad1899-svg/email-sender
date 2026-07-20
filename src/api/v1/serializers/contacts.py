from rest_framework import serializers
from email_sender.models import Contact


class ContactSerializer(serializers.ModelSerializer):
    """
    Сериализатор контактов
    """
    class Meta:
        model = Contact
        fields = (
            "id",
            "name",
            "email",
            "description",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )