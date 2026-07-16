from django.contrib.auth import get_user_model,authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()



#Сериализатор регистрации пользователя
class RegisterSerializer(serializers.ModelSerializer):

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





#Авторизация пользователя по email и паролю
class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):

        email = attrs.get("email")
        password = attrs.get("password")

        try:
            user = User.objects.get(email=email)

        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь не найден.")

        user = authenticate(
            username=user.username,
            password=password
        )
        if user is None:
            raise serializers.ValidationError("Неверный пароль.")
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }




#Сериализатор профиля пользователя
class UserSerializer(serializers.ModelSerializer):


    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "role",
            "is_active",
        )
        read_only_fields = fields