import json


def stringify(iterable):
    return ", ".join(str(item) for item in iterable)


def retrieve_task_parameters(task):
    return json.loads(task.task_params)[1]


def build_event_payload(client, mailing):
    return {
        "event": "newUpdate",
        "botId": client.bot,
        "chatUri": f"id://{client.chat}",
        "data": {"mailing": mailing.name},
    }
