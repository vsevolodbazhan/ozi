from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["POST"])
def echo(request):
    return Response(data=request.data, status=status.HTTP_200_OK)
