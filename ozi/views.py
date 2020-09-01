from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Client, Mailing
from .utilities import stringify


def require_client(request):
    bot = request.data["bot_id"]
    chat = request.data["chat_id"]

    client, _ = Client.objects.get_or_create(bot=bot, chat=chat)

    return client


@api_view(["POST"])
def echo(request):
    return Response(data=request.data, status=status.HTTP_200_OK)


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
