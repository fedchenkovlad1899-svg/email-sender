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
        contact_group = attrs.get("contact_group",getattr(self.instance, "contact_group", None))
        contacts = attrs.get("contacts")
        if contacts is None and self.instance:
            contacts = self.instance.contacts.all()
        if not contact_group and not contacts:
            raise serializers.ValidationError("Выберите получателя сообщения")
        return attrs


    def validate_contact_group(self, value):
        """
        Проверка принадлежности группы контактов пользователю
        """
        if value is None:
            return value
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

    def validate_template(self, value):
        """
        Проверка принадлежности шаблона пользователю
        """
        request = self.context["request"]
        if value.owner != request.user:
            raise serializers.ValidationError("Вы не можете использовать чужой шаблон")
        return value


    def create(self, validated_data):
        """
        создание рассылки.Если указано время отправки,
        рассылка сразу становится запланированной
        """
        if validated_data.get("scheduled_at"):
            validated_data["status"] = (Campaign.SendingStatus.SCHEDULED)
        return super().create(validated_data)



    def update(self, instance, validated_data):
        """
        изменение статуса в зависимости от scheduled_at
        """
        scheduled_at = validated_data.get("scheduled_at",instance.scheduled_at)
        editable_statuses = (
            Campaign.SendingStatus.DRAFT,
            Campaign.SendingStatus.SCHEDULED,
        )

        if instance.status in editable_statuses:
            if scheduled_at:
                validated_data["status"] = (Campaign.SendingStatus.SCHEDULED)
            else:
                validated_data["status"] = (Campaign.SendingStatus.DRAFT)
        return super().update(instance,validated_data)