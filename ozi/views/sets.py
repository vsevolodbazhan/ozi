from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from ..serializers import UserSerializer, MailingSerializer
from ..models import Mailing

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class MailingViewSet(viewsets.ModelViewSet):
    serializer_class = MailingSerializer

    def get_queryset(self):
        user = self.request.user
        return Mailing.objects.filter(user=user)
