from django.urls import path, include

from .api import urls as api_urls
from .tomoru import urls as tomoru_urls

urlpatterns = [path("api/", include(api_urls)), path("tomoru/", include(tomoru_urls))]
