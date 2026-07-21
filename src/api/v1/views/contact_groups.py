from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from api.v1.serializers.contact_groups import ContactGroupSerializer
from email_sender.models import Contact, ContactGroup
from drf_spectacular.utils import extend_schema
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


class ContactGroupListView(generics.ListAPIView):
    """
    Список групп контактов
    """
    serializer_class = ContactGroupSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )
    filterset_fields = ("title",)
    search_fields = ("title","description")
    ordering_fields = ("title","created_at")
    ordering = ("title",)

    def get_queryset(self):
        return ContactGroup.objects.filter(owner=self.request.user)




class ContactGroupCreateView(generics.CreateAPIView):
    """
    Создание группы контактов
    """
    serializer_class = ContactGroupSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)



class ContactGroupRetrieveView(generics.RetrieveAPIView):
    """
    Просмотр группы контактов
    """
    serializer_class = ContactGroupSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ContactGroup.objects.filter(owner=self.request.user)



class ContactGroupUpdateView(generics.UpdateAPIView):
    """
    Изменение группы контактов
    """
    serializer_class = ContactGroupSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ContactGroup.objects.filter(owner=self.request.user)






class ContactGroupDeleteView(generics.DestroyAPIView):
    """
    Удаление группы контактов
    """
    serializer_class = ContactGroupSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ContactGroup.objects.filter(owner=self.request.user)