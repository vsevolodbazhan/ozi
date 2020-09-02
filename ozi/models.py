from django.contrib.auth import get_user_model
from django.db import models

from comparator import distance_is_acceptable, levenshtein_distance, normalize

User = get_user_model()


class Mailing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    @staticmethod
    def find_by_fuzzy_name(name, mailings):
        min_distance = len(name)
        most_similar_mailing = None
        normalized_name = normalize(name)

        for mailing in mailings:
            existing_name = normalize(mailing.name)
            distance = levenshtein_distance(normalized_name, existing_name)
            if distance_is_acceptable(distance) and distance < min_distance:
                min_distance, most_similar_mailing = distance, mailing

        return most_similar_mailing

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (
            "user",
            "name",
        )
        verbose_name = "Mailing"
        verbose_name_plural = "Mailings"


class Client(models.Model):
    bot = models.CharField(max_length=50)
    chat = models.CharField(max_length=50)
    subscriptions = models.ManyToManyField(Mailing)

    def is_subscribed(self, mailing):
        mailings = self.subscriptions.all()
        return mailings.filter(id=mailing.id).exists()

    def __str__(self):
        return f"{self.bot}, {self.chat}"

    class Meta:
        unique_together = (
            "bot",
            "chat",
        )
        verbose_name = "Client"
        verbose_name_plural = "Clients"
