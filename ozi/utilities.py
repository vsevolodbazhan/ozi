import json


def stringify(iterable):
    return ", ".join(str(item) for item in iterable)


def retrieve_task_parameters(task):
    return json.loads(task.task_params)[1]
