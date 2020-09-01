from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Mailing


@api_view(["POST"])
def echo(request):
    return Response(data=request.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def list_mailings(request):
    mailings = Mailing.objects.filter(user=request.user)
    if not mailings:
        return Response(status=status.HTTP_204_NO_CONTENT)

    data = {"mailings": ", ".join(str(mailings) for mailings in mailings)}
    return Response(data=data, status=status.HTTP_200_OK)
