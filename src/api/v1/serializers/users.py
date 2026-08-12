from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from drf_spectacular.utils import extend_schema_serializer


User = get_user_model()

@extend_schema_serializer(component_name="User_RegisterSerializer")
class RegisterSerializer(serializers.ModelSerializer):
    """
    Регистрация пользователя
    """
    password = serializers.CharField(
        write_only=True,
        min_length=8,
    )
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
        )

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                "Пользователь с таким email уже существует"
            )
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


@extend_schema_serializer(component_name="User_LoginSerializer")
class LoginSerializer(serializers.Serializer):
    """
    Авторизация пользователя по email и паролю
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь не найден")

        if not user.check_password(password):
            raise serializers.ValidationError("Неверный пароль")
        if not user.is_active:
            raise serializers.ValidationError("Ваш аккаунт заблокирован.Обратитесь к администратору")
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }


class UserSerializer(serializers.ModelSerializer):
    """
    Профиль пользователя
    """
    role = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "role",
            "date_joined"
        )
        read_only_fields = (
            "id",
            "username",
            "date_joined",
            "is_active",
            "role",
        )

    def get_role(self, user):
        if user.is_superuser:
            return "Администратор"
        return "Пользователь"

@extend_schema_serializer(component_name="User_LogoutSerializer")
class LogoutSerializer(serializers.Serializer):
    """
    Выход
    """
    refresh = serializers.CharField()

    def save(self, **kwargs):
        try:
            token = RefreshToken(self.validated_data["refresh"])
            token.blacklist()
        except (TokenError, Exception):
            raise serializers.ValidationError(
                {"refresh": "проверьте refresh-токен."}
            )

@extend_schema_serializer(component_name="User_ChangePasswordSerializer")
class ChangePasswordSerializer(serializers.Serializer):
    """
    Смена пароля
    """
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True, min_length=8)

    def validate_old_password(self, value):
        # Достаем текущего пользователя из контекста запроса
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Пароль указан неверно")
        return value
    def validate(self, attrs):
        if attrs['old_password'] == attrs['new_password']:
            raise serializers.ValidationError(
                {"new_password": "Новый пароль не должен совпадать со старым"}
            )
        return attrs



#для блокировки

@extend_schema_serializer(component_name="User_StatusSerializer")
class UserStatusSerializer(serializers.ModelSerializer):
    """
    Статус
    """
    class Meta:
        model = User
        fields = (
            "is_active",
        )