from django.contrib import admin

from .models import Client, Mailing

admin.site.register(Client)
admin.site.register(Mailing)
