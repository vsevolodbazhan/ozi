from django.contrib import admin

from .models import Client, Hook, Mailing, Update


class UpdateAdmin(admin.ModelAdmin):
    readonly_fields = ("user", "mailing", "client", "time", "date", "repeat")


admin.site.register(Client)
admin.site.register(Hook)
admin.site.register(Mailing)
admin.site.register(Update, UpdateAdmin)
