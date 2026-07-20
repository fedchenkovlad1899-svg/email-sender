from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from email_sender.models import Contact
from api.v1.serializers.contacts import ContactSerializer
from email_sender.models import Contact
from drf_spectacular.utils import extend_schema

#GET /contact/list
@extend_schema(tags=['Contact'])
class ContactListView(generics.ListAPIView):
    """
    Cписок контактов  активного пользователя
    """
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Contact.objects.filter(owner=self.request.user)


#POST /contacts/create/
@extend_schema(tags=['Contact'])
class ContactCreateView(generics.CreateAPIView):
    """
    Создание нового контакта
    """
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)#владелец-кто вошел в систему


#GET /contacts/{id}/
@extend_schema(tags=['Contact'])
class ContactRetrieveView(generics.RetrieveAPIView):
    """
    Просмотр определенного контакта активного пользователя
    """
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Contact.objects.filter(owner=self.request.user)


#PUT/PATCH /contacts/{id}/update/
@extend_schema(tags=['Contact'])
class ContactUpdateView(generics.UpdateAPIView):
    """
    Изменение контакта
    """
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Contact.objects.filter(owner=self.request.user)


#DELETE /contacts/{id}/delete/
@extend_schema(tags=['Contact'])
class ContactDeleteView(generics.DestroyAPIView):
    """
    Удаление контакта
    """
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Contact.objects.filter(owner=self.request.user)