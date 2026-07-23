from rest_framework import serializers
from email_sender.models import Contact
from drf_spectacular.utils import extend_schema_serializer

@extend_schema_serializer(component_name="ContactSerializer")
class ContactSerializer(serializers.ModelSerializer):
    """
    Контакты
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


@extend_schema_serializer(component_name="ContactImportSerializer")
class ContactImportSerializer(serializers.Serializer):
    """
    Загрузка контактов из CSV или XLSX
    """
    file = serializers.FileField()
    group_id = serializers.IntegerField(
        required=False,
        allow_null=True,
    )
    def validate_file(self, file):
        filename = file.name.lower()
        if not filename.endswith((".csv", ".xlsx")):
            raise serializers.ValidationError("поддерживаются только CSV и XLSX файлы")

        max_size = 5 * 1024 * 1024
        if file.size > max_size:
            raise serializers.ValidationError("Размер файла не должен превышать 5 МБ"
            )
        return file
