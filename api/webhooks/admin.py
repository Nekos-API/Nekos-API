from django.contrib import admin

from webhooks.models import Webhook

# Register your models here.


class WebhookAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "events")
    raw_id_fields = ("user",)


admin.site.register(Webhook, WebhookAdmin)
