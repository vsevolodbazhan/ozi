from datetime import date as _date
from datetime import datetime
from datetime import time as _time
from datetime import timedelta

from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response

from sheets import extract_values

from . import exceptions
from .constants import NUMBER_OF_SECONDS_IN_MINUTE
from .models import Client, Hook, Mailing
from .tasks import send_event
from .utilities import stringify


def require_client(request):
    bot = request.data["bot_id"]
    chat = request.data["chat_id"]

    client, _ = Client.objects.get_or_create(bot=bot, chat=chat)

    return client


def require_mailing(request):
    mailing_id = request.data["mailing_id"]

    try:
        mailing = Mailing.objects.get(id=mailing_id)
    except Mailing.DoesNotExist:
        raise exceptions.NotFound("Could not find a mailing with the provided ID.")

    return mailing


@api_view(["POST"])
@authentication_classes([])
def create_hook(request):
    target = request.data["tomoru_callback_url"]

    Hook.objects.create(target=target)

    return Response(status=status.HTTP_201_CREATED)


@api_view(["POST"])
def list_mailings(request):
    mailings = Mailing.objects.filter(user=request.user, common=True)

    if not mailings:
        return Response(status=status.HTTP_204_NO_CONTENT)

    data = {"mailings": stringify(mailings)}
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(["POST"])
def list_client_subscriptions(request):
    client = require_client(request)
    subscriptions = client.subscriptions.all()

    if not subscriptions:
        return Response(status=status.HTTP_204_NO_CONTENT)

    data = {"subscriptions": stringify(subscriptions)}
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(["POST"])
def subscribe_client(request):
    client = require_client(request)
    mailing = require_mailing(request)

    if client.is_subscribed(mailing):
        raise exceptions.Conflict("Client is already subscribed.")

    client.subscriptions.add(mailing)
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
def unsubscribe_client(request):
    client = require_client(request)
    mailing = require_mailing(request)

    if not client.is_subscribed(mailing):
        raise exceptions.Conflict("Client is not subscribed.")

    client.subscriptions.remove(mailing)
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
def find_mailing(request):
    name = request.data["name"]
    mailings = Mailing.objects.filter(user=request.user, common=True)

    most_similar_mailing = Mailing.find_by_fuzzy_name(name, mailings)
    if most_similar_mailing is None:
        raise exceptions.NotFound("Couldn't find a relevant subscription.")

    data = {"mailing_id": most_similar_mailing.id}
    return Response(data=data, status=status.HTTP_200_OK)


def update_for_all(request, callback):
    user = request.user
    mailing = require_mailing(request)

    if chats := request.data.get("chats"):
        bot = request.data["bot_id"]
        clients = []
        for chat in chats.split(", "):
            client, _ = Client.objects.get_or_create(bot=bot, chat=chat)
            client.subscriptions.add(mailing)
            clients.append(client)
    else:
        clients = Client.objects.get_subscribed(mailing)

    return callback(user, mailing, clients, parameters=request.data)


def update_for_client(request, callback):
    user = request.user
    mailing = require_mailing(request)
    client = require_client(request)

    return callback(user, mailing, clients=[client], parameters=request.data)


def plan_updates(user, mailing, clients, parameters):
    hours = parameters.get("hours", 0)
    minutes = parameters.get("minutes", 0)

    timestamp = timezone.now() + timedelta(hours=hours, minutes=minutes)

    for client in clients:
        send_event(
            user_id=str(user.id),
            mailing_id=str(mailing.id),
            client_id=str(client.id),
            schedule=timestamp,
        )
    return Response(status=status.HTTP_202_ACCEPTED)


@api_view(["POST"])
def plan_update_for_all(request):
    return update_for_all(request, plan_updates)


@api_view(["POST"])
def plan_update_for_client(request):
    return update_for_client(request, plan_updates)


def schedule_updates(user, mailing, clients, parameters):
    time = parameters.get("time")
    date = parameters.get("date")
    repeat = parameters.get("repeat", 0) * NUMBER_OF_SECONDS_IN_MINUTE

    time, date = (
        timezone.now().time() if time is None else _time.fromisoformat(time),
        timezone.now().date() if date is None else _date.fromisoformat(date),
    )
    timestamp = timezone.make_aware(datetime.combine(date=date, time=time))

    for client in clients:
        send_event(
            user_id=str(user.id),
            mailing_id=str(mailing.id),
            client_id=str(client.id),
            schedule=timestamp,
            repeat=repeat,
        )
    return Response(status=status.HTTP_202_ACCEPTED)


@api_view(["POST"])
def schedule_update_for_all(request):
    return update_for_all(request, schedule_updates)


@api_view(["POST"])
def schedule_update_for_client(request):
    return update_for_client(request, schedule_updates)


@api_view(["POST"])
def extract_chats_from_sheet(request):
    values = extract_values(
        spreadsheet_id=request.data["spreadsheet_id"],
        column=request.data["column"],
        range_start=request.data["range_start"],
        range_end=request.data["range_end"],
    )

    if values is None:
        return Response(status=status.HTTP_204_NO_CONTENT)

    data = {"chats": stringify(values)}
    return Response(data=data, status=status.HTTP_200_OK)
