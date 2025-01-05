from django.contrib import admin

from .models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("id", "rating", "artist_name", "source_name", "source_id")
    list_filter = ("rating",)
    search_fields = ("artist_name", "source_name", "source_id")
