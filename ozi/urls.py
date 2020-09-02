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
    path("find-mailing", views.find_mailing, name="find-mailing"),
    path("plan-update", views.plan_update, name="plan-update"),
    path("schedule-update", views.schedule_update, name="schedule-update"),
]
