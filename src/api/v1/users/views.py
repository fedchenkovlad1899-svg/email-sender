from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser,AllowAny
from rest_framework.generics import ListAPIView
from users.models import User
from api.v1.users.serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserSerializer,
    LogoutSerializer,
    ChangePasswordSerializer,
    UserStatusSerializer
)


#POST /api/users/register/
class RegisterView(generics.CreateAPIView):
    """
    Регистрация пользователя
    """
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]



#POST /api/users/login/
class LoginView(generics.GenericAPIView):
    """
    Авторизация пользователя по email и паролю
    """
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data) #получаем json из запроса
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)



#GET/PUT/PATCH  /api/users/profile/
class ProfileView(generics.RetrieveUpdateAPIView):
    """
    Просмотр и изменение профиля пользователя
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


#POST /api/users/logout/
class LogoutView(generics.GenericAPIView):
    """
    Выход пользователя
    """
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "Вы вышли из системы."},
            status=status.HTTP_205_RESET_CONTENT
        )

#POST /api/users/change_password/
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
        return Response(
            {"detail": "Пароль успешно изменен."},
            status=status.HTTP_200_OK
        )


#для админа

#GET  /api/users/profiles/
class UserListView(generics.ListAPIView):
    """
    Вывод списка всех пользователей
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

#GET  /api/users/users{id}/
class UserDetailView(generics.RetrieveAPIView):
    """
    Просмотр пользователя администратором
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

#PUT/PATCH  /api/users/users{id}/status
class UserStatusView(generics.UpdateAPIView):
    """
    Блокировка/разблокировка пользователя
    """
    queryset = User.objects.all()
    serializer_class = UserStatusSerializer
    permission_classes = [IsAdminUser]

#DELETE  /api/users/users{id}/delete
class UserDeleteView(generics.DestroyAPIView):
    """
    Удаление пользователя
    """
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]