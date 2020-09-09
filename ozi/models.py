import uuid

from background_task.models import Task
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .comparator import distance_is_acceptable, levenshtein_distance, normalize
from .constants import NUMBER_OF_SECONDS_IN_MINUTE
from .utilities import retrieve_task_parameters

User = get_user_model()


class Mailing(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    common = models.BooleanField(default=True)

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


class ClientManager(models.Manager):
    def get_subscribed(self, mailings):
        return self.filter(subscriptions__in=mailings).distinct()


class Client(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bot = models.CharField(max_length=50)
    chat = models.CharField(max_length=50)
    subscriptions = models.ManyToManyField(Mailing)

    objects = ClientManager()

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


class Hook(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    target = models.URLField(max_length=500)

    def __str__(self):
        return self.target

    class Meta:
        verbose_name = "Hook"
        verbose_name_plural = "Hooks"


class Update(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, editable=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True, null=True)

    time = models.TimeField()
    date = models.DateField()
    repeat = models.CharField(max_length=25, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.time = self.task.run_at.time()
        self.date = self.task.run_at.date()
        if self.task.repeat > 0:
            self.repeat = (
                f"Every {self.task.repeat // NUMBER_OF_SECONDS_IN_MINUTE} minute(s)"
            )
        super(Update, self).save(*args, **kwargs)

    def __str__(self):
        parameters = f"{self.time}, {self.date}"
        if self.client is not None:
            parameters = f"{parameters}, {self.client}"

        return f"{self.mailing} ({parameters})"

    class Meta:
        verbose_name = "Update"
        verbose_name_plural = "Updates"


@receiver(post_save, sender=Task)
def create_update(sender, instance, created=False, **kwargs):
    if not created:
        return

    parameters = retrieve_task_parameters(instance)

    user = User.objects.get(id=parameters["user_id"])
    mailing = Mailing.objects.get(id=parameters["mailing_id"])

    client = None
    if client_id := parameters.get("client_id"):
        client = Client.objects.get(id=client_id)

    Update.objects.create(task=instance, user=user, mailing=mailing, client=client)


@receiver(post_delete, sender=Update)
def delete_task(sender, instance, **kwargs):
    instance.task.delete()
