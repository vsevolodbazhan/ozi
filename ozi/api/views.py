from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAdminUser

from config.utilities import get_user_model

from ..models import Client, Mailing, Update
from ..serializers import (
    ClientSerializer,
    MailingSerializer,
    UpdateSerializer,
    UserSerializer,
)

User = get_user_model()


class CreateWithUserMixin:
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer

    def get_queryset(self):
        user = self.request.user
        mailings = Mailing.objects.filter(user=user)
        return Client.objects.get_subscribed(mailings)


class MailingViewSet(CreateWithUserMixin, viewsets.ModelViewSet):
    serializer_class = MailingSerializer

    def get_queryset(self):
        user = self.request.user
        return Mailing.objects.filter(user=user)


class UpdateViewSet(
    CreateWithUserMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = UpdateSerializer

    def get_queryset(self):
        user = self.request.user
        return Update.objects.filter(user=user)
