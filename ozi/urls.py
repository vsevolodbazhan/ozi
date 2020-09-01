from django.urls import path

from .views import echo, list_mailings

urlpatterns = [
    path("echo", echo),
    path("mailings", list_mailings, name="list-mailings"),
]
