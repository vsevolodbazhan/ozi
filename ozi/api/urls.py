from rest_framework import routers

from . import views

router = routers.SimpleRouter(trailing_slash=False)
router.register(r"users", views.UserViewSet, basename="user")
router.register(r"clients", views.ClientViewSet, basename="client")
router.register(r"mailings", views.MailingViewSet, basename="mailing")

urlpatterns = router.urls
