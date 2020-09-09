from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from ..models import Client, Mailing
from ..serializers import ClientSerializer, MailingSerializer, UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer

    def get_queryset(self):
        user = self.request.user
        mailings = Mailing.objects.filter(user=user)
        return Client.objects.get_subscribed(mailings)


class MailingViewSet(viewsets.ModelViewSet):
    serializer_class = MailingSerializer

    def get_queryset(self):
        user = self.request.user
        return Mailing.objects.filter(user=user)
