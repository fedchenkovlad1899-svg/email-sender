from django.contrib.auth import get_user_model,authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

User = get_user_model()




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

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)



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
        user = authenticate(
            username=user.username,
            password=password
        )
        if user is None:
            raise serializers.ValidationError("Неверный пароль")
        if not user.is_active:
            raise serializers.ValidationError(
                "Ваш аккаунт заблокирован.Обратитесь к администратору"
            )
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }



class UserSerializer(serializers.ModelSerializer):
    """
    Профиль пользователя
    """
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "role",
            "is_active",
            "date_joined"
        )
        read_only_fields = (
            "id",
            "email",
            "date_joined",
        )


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
class UserStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "is_active",
        )