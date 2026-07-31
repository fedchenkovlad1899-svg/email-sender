from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from api.v1.serializers.contacts import ContactSerializer,ContactImportSerializer
from email_sender.models import Contact,ContactGroup
from email_sender.services.contact_import import import_contacts
from drf_spectacular.utils import extend_schema
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.parsers import MultiPartParser, FormParser


#GET /contacts/list
@extend_schema(tags=['Contact'])
class ContactListView(generics.ListAPIView):
    """
    Cписок контактов  активного пользователя
    """
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )
    filterset_fields = (
        "email",
        "name",
        "created_at",
    )
    search_fields = (
        "name",
        "email",
        "description",
    )
    ordering_fields = (
        "name",
        "created_at",
    )
    ordering = ("name",)
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
@extend_schema(
    tags=['Contact'],
    request=None,
    responses={204: None}
)
class ContactDeleteView(generics.DestroyAPIView):
    """
    Удаление контакта
    """
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Contact.objects.filter(owner=self.request.user)


@extend_schema(tags=["Contact"],request=ContactImportSerializer)
class ContactImportView(APIView):
    """
    Импорт контактов из CSV или XLSX файла
    """
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser,FormParser]
    def post(self, request):
        serializer = ContactImportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data["file"]
        group_id = serializer.validated_data.get("group_id")
        group = None

        if group_id is not None:
            try:
                group = ContactGroup.objects.get(id=group_id,owner=request.user)
            except ContactGroup.DoesNotExist:
                return Response({"detail": "Группа не найдена или не принадлежит пользователю"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        try:
            result = import_contacts(
                file=file,
                owner=request.user,
                group=group,
            )
        except ValueError as error:
            return Response({"detail": str(error)},status=status.HTTP_400_BAD_REQUEST)
        return Response(result,status=status.HTTP_201_CREATED)