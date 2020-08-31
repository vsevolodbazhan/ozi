from http import HTTPStatus as status

from django.http import JsonResponse


def hello(request):
    data = {"message": "Hello!"}
    return JsonResponse(data=data, status=status.OK)
