from rest_framework import serializers
from email_sender.models import Campaign



class CampaignSerializer(serializers.ModelSerializer):
    """
    Рассылки
    """
    class Meta:
        model = Campaign
        fields = (
            "id",
            "title",
            "template",
            "contact_group",
            "contacts",
            "scheduled_at",
            "status",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "status",
            "created_at",
            "updated_at",
        )


    def validate(self, attrs):
        """
        Проверка получателей рассылки
        """
        contact_group = attrs.get("contact_group")
        contacts = attrs.get("contacts")
        if not contact_group and not contacts:
            raise serializers.ValidationError("Выберите получателя сообщения")
        return attrs


    def validate_contact_group(self, value):
        """
        Проверка принадлежности группы контактов пользователю
        """
        request = self.context["request"]
        if value.owner != request.user:
            raise serializers.ValidationError("Вы не можете использовать чужую группу контактов")
        return value


    def validate_contacts(self, value):
        """
        Проверка принадлежности контактов пользователю
        """
        request = self.context["request"]
        for contact in value:
            if contact.owner != request.user:
                raise serializers.ValidationError(f"Контакт '{contact}' вам не принадлежит")
        return value

    def validate_message_template(self, value):
        """
        Проверка принадлежности шаблона пользователю
        """
        request = self.context["request"]
        if value.owner != request.user:
            raise serializers.ValidationError("Вы не можете использовать чужой шаблон")
        return value