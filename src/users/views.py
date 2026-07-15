from rest_framework import generics
from users.serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    """
    Регистрация пользователя
    """

    serializer_class = RegisterSerializer