from django.urls import path

from . import views

urlpatterns = [
    path("mailings", views.list_mailings, name="list-mailings"),
    path(
        "subscriptions",
        views.list_client_subscriptions,
        name="list-subscriptions",
    ),
]
