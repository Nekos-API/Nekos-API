from django.contrib import admin

from gifs.models import Gif, Reaction

# Register your models here.


class GifAdmin(admin.ModelAdmin):
    list_display = ("id", "emotions", "is_spoiler", "uploader")
    list_filter = ("reactions", "emotions", "is_spoiler", "uploader")
    search_fields = (
        "text",
        "uploader",
        "reactions",
        "emotions",
        "characters",
        "categories",
    )
    autocomplete_fields = ["characters", "categories", "reactions"]
    readonly_fields = [
        "id",
        "height",
        "width",
        "aspect_ratio",
        "orientation",
        "duration",
        "frames",
        "mimetype",
        "palette",
        "dominant_color",
        "created_at",
        "updated_at",
    ]
    raw_id_fields = ["uploader"]


class ReactionAdmin(admin.ModelAdmin):
    list_display = ("name", "is_nsfw", "id")
    list_filter = ("is_nsfw",)
    search_fields = ("name",)


admin.site.register(Gif, GifAdmin)
admin.site.register(Reaction, ReactionAdmin)
