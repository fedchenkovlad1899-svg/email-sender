from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from api.v1.serializers.email_logs import EmailLogSerializer
from email_sender.models import EmailLog
from drf_spectacular.utils import extend_schema
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


@extend_schema(tags=['Logs'])
class EmailLogListView(generics.ListAPIView):
    """
    Список логов отправки писем
    """
    serializer_class = EmailLogSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )
    filterset_fields = ("status",)
    search_fields = (
        "contact__email",
        "campaign__title",
    )
    ordering_fields = (
        "created_at",
        "sent_at",
    )
    ordering = ("-created_at",)

    def get_queryset(self):
        return EmailLog.objects.filter(campaign__owner=self.request.user)




@extend_schema(tags=['Logs'])
class EmailLogRetrieveView(generics.RetrieveAPIView):
    """
    Просмотр определенных логов
    """
    serializer_class = EmailLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return EmailLog.objects.filter(campaign__owner=self.request.user)