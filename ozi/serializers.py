from datetime import datetime

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers

from .constants import NUMBER_OF_SECONDS_IN_MINUTE
from .models import Client, Mailing, Update
from .tasks import send_event

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
    class Meta:
        model = Client
        fields = ["id", "bot", "chat", "subscriptions"]


class MailingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mailing
        fields = ["id", "name", "common"]


class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Update
        fields = ["id", "mailing", "client", "time", "date", "repeat"]

    def validate(self, data):
        time, date = data.pop("time"), data.pop("date")
        schedule = timezone.make_aware(datetime.combine(date, time))

        if schedule < timezone.now():
            raise serializers.ValidationError(
                "Can not schedule an update earlier than now."
            )

        data["schedule"] = schedule
        return data

    def create(self, data):
        task_parameters = {
            "user_id": str(data["user"].id),
            "mailing_id": str(data["mailing"].id),
            "client_id": str(data["client"].id),
            "schedule": data["schedule"],
            "repeat": data["repeat"] * NUMBER_OF_SECONDS_IN_MINUTE,
        }
        task = send_event(**task_parameters)
        return Update.objects.get(task=task)
