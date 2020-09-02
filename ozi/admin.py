from django.contrib import admin

from .models import Client, Mailing, Update


class UpdateAdmin(admin.ModelAdmin):
    readonly_fields = ("user", "mailing", "client", "time", "date")


admin.site.register(Client)
admin.site.register(Mailing)
admin.site.register(Update, UpdateAdmin)
