from django.urls import include, path
from rest_framework import routers

from .views import operations as ops
from .views import sets

operation_patterns = [
    path("create-hook", ops.create_hook, name="create-hook"),
    path(
        "extract-chats", ops.extract_chats_from_sheet, name="extract-chats-from-sheet"
    ),
    path("find-mailing", ops.find_mailing, name="find-mailing"),
    path(
        "subscriptions",
        ops.list_client_subscriptions,
        name="list-client-subscriptions",
    ),
    path("mailings", ops.list_mailings, name="list-mailings"),
    path(
        "plan-updates",
        ops.plan_update_for_all,
        name="plan-update-for-all",
    ),
    path(
        "plan-update",
        ops.plan_update_for_client,
        name="plan-update-for-client",
    ),
    path(
        "schedule-updates",
        ops.schedule_update_for_all,
        name="schedule-update-for-all",
    ),
    path(
        "schedule-update",
        ops.schedule_update_for_client,
        name="schedule-update-for-client",
    ),
    path("subscribe", ops.subscribe_client, name="subscribe-client"),
    path("unsubscribe", ops.unsubscribe_client, name="unsubscribe-client"),
]

router = routers.SimpleRouter(trailing_slash=False)
router.register(r"users", sets.UserViewSet, basename="user")
router.register(r"clients", sets.ClientViewSet, basename="client")
router.register(r"mailings", sets.MailingViewSet, basename="mailing")

urlpatterns = [
    path("", include(router.urls)),
    path("operations/", include(operation_patterns)),
]
