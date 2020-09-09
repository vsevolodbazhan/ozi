from django.urls import path

from . import views

urlpatterns = [
    path(
        "create-hook",
        views.create_hook,
        name="create-hook",
    ),
    path(
        "extract-chats",
        views.extract_chats_from_sheet,
        name="extract-chats-from-sheet",
    ),
    path(
        "find-mailing",
        views.find_mailing,
        name="find-mailing",
    ),
    path(
        "subscriptions",
        views.list_client_subscriptions,
        name="list-client-subscriptions",
    ),
    path(
        "mailings",
        views.list_mailings,
        name="list-mailings",
    ),
    path(
        "plan-updates",
        views.plan_update_for_all,
        name="plan-update-for-all",
    ),
    path(
        "plan-update",
        views.plan_update_for_client,
        name="plan-update-for-client",
    ),
    path(
        "schedule-updates",
        views.schedule_update_for_all,
        name="schedule-update-for-all",
    ),
    path(
        "schedule-update",
        views.schedule_update_for_client,
        name="schedule-update-for-client",
    ),
    path(
        "subscribe",
        views.subscribe_client,
        name="subscribe-client",
    ),
    path(
        "unsubscribe",
        views.unsubscribe_client,
        name="unsubscribe-client",
    ),
]