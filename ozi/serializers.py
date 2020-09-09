from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Mailing

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "date_joined",
            "is_active",
            "is_staff",
            "password",
        ]
        read_only_fields = ["date_joined"]
        extra_kwargs = {"password": {"write_only": True}}


class MailingSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField(source="user")

    class Meta:
        model = Mailing
        fields = ["id", "user_id", "name", "common"]
