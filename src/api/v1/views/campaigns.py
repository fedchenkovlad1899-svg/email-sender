from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from api.v1.serializers.campaigns import CampaignSerializer
from email_sender.models import Campaign
from email_sender.tasks import send_campaign_task
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



@extend_schema(tags=["Campaign"],request=None,)  #post ничего не принимает
class CampaignSendView(generics.GenericAPIView):
    """
    Запуск рассылки через celery
    """
    serializer_class = CampaignSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        """
        Пользователь может запускать только свои рассылки
        """
        return Campaign.objects.filter(owner=self.request.user)

    def post(self, request, pk):
        """
        Ставит выбранную рассылку в очередь celery
        """
        campaign = self.get_object()  #pk из URL и поиск объекта в get_queryset()
        allowed_statuses = (
            Campaign.SendingStatus.DRAFT,
            Campaign.SendingStatus.SCHEDULED,
            Campaign.SendingStatus.FAILED,
        )
        if campaign.status not in allowed_statuses:
            return Response(
                {
                    "detail": (
                    f'Рассылку со статусом "{campaign.get_status_display()}" нельзя запустить'
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        task = send_campaign_task.delay(campaign.id) #в redis send_campaign_task(campaign.id)- worker send_campaign(campaign)
        return Response(
            {
                "detail": "Рассылка поставлена в очередь",
                "campaign_id": campaign.id,
                "task_id": task.id,
            },
            status=status.HTTP_202_ACCEPTED,
        )




@extend_schema(tags=["Campaign"],request=None)
class CampaignCancelView(generics.GenericAPIView):
    """
    Отмена запланированной рассылки
    """
    serializer_class = CampaignSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Пользователь может отменять только свои рассылки
        """
        return Campaign.objects.filter(owner=self.request.user)

    def post(self, request, pk):
        """
        Переводит рассылку SCHEDULED в статус CANCELED
        """
        campaign = self.get_object()
        if campaign.status != Campaign.SendingStatus.SCHEDULED:
            return Response(
                {
                    "detail": (
                        "Отменить можно только рассылку со статусом Запланирована"
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        campaign.status = Campaign.SendingStatus.CANCELED
        campaign.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )
        return Response(
            {
                "detail": "Рассылка успешно отменена",
                "campaign_id": campaign.id,
                "status": campaign.status,
            },
            status=status.HTTP_200_OK,
        )





@extend_schema(tags=['Campaign'])
class CampaignDeleteView(generics.DestroyAPIView):
    """
    Удаление рассылки
    """
    serializer_class = CampaignSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Campaign.objects.filter(
            owner=self.request.user,
            status__in=(
                Campaign.SendingStatus.DRAFT,
                Campaign.SendingStatus.CANCELED,
            )
        )