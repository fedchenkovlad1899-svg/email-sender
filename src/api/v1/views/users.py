from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser,AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import ListAPIView,RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User
from drf_spectacular.utils import extend_schema
from api.v1.serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserSerializer,
    LogoutSerializer,
    ChangePasswordSerializer,
    UserStatusSerializer
)


@extend_schema(tags=['User'])
class RegisterView(generics.CreateAPIView):
    """
    Регистрация пользователя и автологин
    """
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": UserSerializer(user).data,
            },
            status=status.HTTP_201_CREATED,
        )



@extend_schema(tags=['User'])
class LoginView(generics.GenericAPIView):
    """
    Аутентификация пользователя по email и паролю
    """
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data) #получаем json из запроса
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)



@extend_schema(tags=['User'])
class ProfileView(generics.RetrieveUpdateAPIView):
    """
    Просмотр и изменение профиля пользователя
    """
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]  #чтобы работало без авторизированной админки по JWT
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


@extend_schema(tags=['User'])
class LogoutView(generics.GenericAPIView):
    """
    Выход пользователя
    """
    serializer_class = LogoutSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Вы вышли из системы."},status=status.HTTP_205_RESET_CONTENT)


@extend_schema(tags=['User'])
class ChangePasswordView(generics.GenericAPIView):
    """
    Смена пароля
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        user.set_password(serializer.validated_data["new_password"])
        user.save()
        return Response({"detail": "Пароль успешно изменен."},status=status.HTTP_200_OK)


#для админа


@extend_schema(tags=['Admin_only'])
class UserListView(generics.ListAPIView):
    """
    Вывод списка всех пользователей
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

@extend_schema(tags=['Admin_only'])
class UserDetailView(generics.RetrieveAPIView):
    """
    Просмотр пользователя администратором
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


@extend_schema(tags=['Admin_only'])
class UserStatusView(generics.UpdateAPIView):
    """
    Блокировка/разблокировка пользователя
    """
    queryset = User.objects.all()
    serializer_class = UserStatusSerializer
    permission_classes = [IsAdminUser]


@extend_schema(
    tags=['Admin_only'],
    request=None,          #чтобы убрать ошибку.тк не задаем сериалайзер
    responses={204: None}
)
class UserDeleteView(generics.DestroyAPIView):
    """
    Удаление пользователя
    """
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]

