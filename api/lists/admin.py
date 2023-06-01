from django.contrib import admin

from .models import List

# Register your models here.


class ListAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "is_private")
    list_filter = ("is_private",)
    raw_id_fields = ("user",)
    autocomplete_fields = ("images",)


admin.site.register(List, ListAdmin)
