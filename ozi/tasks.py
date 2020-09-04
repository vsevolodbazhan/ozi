import requests
from background_task import background

from .models import Client, Hook, Mailing
from .utilities import build_event_payload


@background
def send_event(user_id, mailing_id, client_id=None):
    mailing = Mailing.objects.get(id=mailing_id)

    if client_id is None:
        clients = Client.objects.get_subscribed(mailing)
    else:
        clients = Client.objects.filter(id=client_id)

    hooks = Hook.objects.all()
    for client in clients:
        for hook in hooks:
            payload = build_event_payload(client=client, mailing=mailing)
            requests.post(hook.target, json=payload)
