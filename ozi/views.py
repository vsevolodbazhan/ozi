from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Client, Mailing
from .utilities import stringify
from . import exceptions


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
def list_mailings(request):
    mailings = Mailing.objects.filter(user=request.user)

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
