from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Mailing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (
            "user",
            "name",
        )
        verbose_name = "mailing"
        verbose_name_plural = "mailing"


class Client(models.Model):
    bot = models.CharField(max_length=50)
    chat = models.CharField(max_length=50)
    subscriptions = models.ManyToManyField(Mailing)

    def __str__(self):
        return f"{self.bot}, {self.chat}"

    class Meta:
        unique_together = (
            "bot",
            "chat",
        )
        verbose_name = "client"
        verbose_name_plural = "clients"
