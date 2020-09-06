import requests
from background_task import background

from .models import Client, Hook, Mailing
from .utilities import build_event_payload


@background
def send_event(user_id, mailing_id, client_id):
    mailing = Mailing.objects.get(id=mailing_id)
    client = Client.objects.get(id=client_id)
    hooks = Hook.objects.all()

    for hook in hooks:
        payload = build_event_payload(client=client, mailing=mailing)
        requests.post(hook.target, json=payload)
