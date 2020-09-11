from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.views.generic import TemplateView

from .api import urls as api_urls
from .tomoru import urls as tomoru_urls

urlpatterns = [
    path("api/", include(api_urls)),
    path("tomoru/", include(tomoru_urls)),
    path("docs/", TemplateView.as_view(template_name="docs.html")),
] + static(settings.STATIC_URL)
