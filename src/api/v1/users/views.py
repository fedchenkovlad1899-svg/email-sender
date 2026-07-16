from rest_framework import generics,status
from rest_framework.response import Response
from api.v1.users.serializers import RegisterSerializer,LoginSerializer,UserSerializer
from rest_framework.permissions import IsAuthenticated



#POST /api/users/register/
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

#POST /api/users/login/
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data) #получаем json из запроса
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)



#GET  /api/users/profile/
class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user