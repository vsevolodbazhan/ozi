from django.urls import path

from . import views

urlpatterns = [
    path("mailings", views.list_mailings, name="list-mailings"),
    path(
        "subscriptions",
        views.list_client_subscriptions,
        name="list-subscriptions",
    ),
    path("subscribe", views.subscribe_client, name="subscribe-client"),
    path("unsubscribe", views.unsubscribe_client, name="unsubscribe-client"),
]
