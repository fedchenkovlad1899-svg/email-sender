from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from api.v1.serializers.message_templates import MessageTemplateSerializer
from email_sender.models import MessageTemplate
from drf_spectacular.utils import extend_schema
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_spectacular.utils import extend_schema

@extend_schema(tags=['Message'])
class MessageTemplateListView(generics.ListAPIView):
    """
    Список шаблонов текущего пользователя
    """
    serializer_class = MessageTemplateSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )
    filterset_fields = (
        "title",
        "subject",
    )
    search_fields = (
        "title",
        "subject",
        "body",
    )
    ordering_fields = (
        "title",
        "subject",
        "created_at",
    )
    ordering = ("title",)
    def get_queryset(self):
        return MessageTemplate.objects.filter(owner=self.request.user)


@extend_schema(tags=['Message'])
class MessageTemplateCreateView(generics.CreateAPIView):
    """
    Создание шаблона письма
    """
    serializer_class = MessageTemplateSerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


@extend_schema(tags=['Message'])
class MessageTemplateRetrieveView(generics.RetrieveAPIView):
    """
    Просмотр шаблона
    """
    serializer_class = MessageTemplateSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return MessageTemplate.objects.filter(owner=self.request.user)


@extend_schema(tags=['Message'])
class MessageTemplateUpdateView(generics.UpdateAPIView):
    """
    Изменение шаблона
    """
    serializer_class = MessageTemplateSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return MessageTemplate.objects.filter(owner=self.request.user)


@extend_schema(tags=['Message'])
class MessageTemplateDeleteView(generics.DestroyAPIView):
    """
    Удаление шаблона
    """
    serializer_class = MessageTemplateSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return MessageTemplate.objects.filter(owner=self.request.user)