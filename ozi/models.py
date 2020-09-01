from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Mailing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "mailing"
        verbose_name_plural = "mailing"
