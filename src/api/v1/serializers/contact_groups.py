from rest_framework import serializers
from email_sender.models import ContactGroup


class ContactGroupSerializer(serializers.ModelSerializer):
    """
    Группы контактов
    """
    class Meta:
        model = ContactGroup
        fields = (
            "id",
            "title",
            "description",
            "contacts",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )