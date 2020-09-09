from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers

from .models import Client, Mailing

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


class ClientSerializer(serializers.ModelSerializer):
    bot_id = serializers.CharField(source="bot")
    chat_id = serializers.CharField(source="chat")

    class Meta:
        model = Client
        fields = ["id", "bot_id", "chat_id", "subscriptions"]


class MailingSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField(source="user")

    class Meta:
        model = Mailing
        fields = ["id", "user_id", "name", "common"]


def almost_now(offset_in_seconds=5):
    return timezone.now() + timedelta(seconds=offset_in_seconds)


class UpdateSerializer(serializers.Serializer):
    mailing_id = serializers.UUIDField()
    client_id = serializers.UUIDField()
    schedule = serializers.DateTimeField(required=False, default=almost_now())
    repeat = serializers.IntegerField(min_value=0, required=False, default=0)

    def validate_schedule(self, value):
        if value < timezone.now():
            raise serializers.ValidationError(
                "Can not schedule an update earlier than now."
            )

        return value
