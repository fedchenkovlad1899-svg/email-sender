from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from api.v1.serializers.campaigns import CampaignSerializer
from email_sender.models import Campaign
from drf_spectacular.utils import extend_schema
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

@extend_schema(tags=['Campaign'])
class CampaignListView(generics.ListAPIView):
    """
    Список рассылок пользователя
    """
    serializer_class = CampaignSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )
    filterset_fields = ("status",)
    search_fields = ("title",)
    ordering_fields = (
        "title",
        "scheduled_at",
        "created_at",
    )
    ordering = ("-created_at",)

    def get_queryset(self):
        return Campaign.objects.filter(owner=self.request.user)


@extend_schema(tags=['Campaign'])
class CampaignCreateView(generics.CreateAPIView):
    """
    Создание рассылки
    """
    serializer_class = CampaignSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


@extend_schema(tags=['Campaign'])
class CampaignRetrieveView(generics.RetrieveAPIView):
    """
    Просмотр информации о рассылке
    """
    serializer_class = CampaignSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Campaign.objects.filter(owner=self.request.user)



@extend_schema(tags=['Campaign'])
class CampaignUpdateView(generics.UpdateAPIView):
    """
    Изменение рассылки
    """
    serializer_class = CampaignSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Campaign.objects.filter(owner=self.request.user)


@extend_schema(tags=['Campaign'])
class CampaignDeleteView(generics.DestroyAPIView):
    """
    Удаление рассылки
    """
    serializer_class = CampaignSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Campaign.objects.filter(owner=self.request.user)