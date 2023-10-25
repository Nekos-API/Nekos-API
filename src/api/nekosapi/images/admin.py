from django.contrib import admin

from nekosapi.images.models import Image, Tag


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "artist",
        "verification",
        "rating",
        "image_height",
        "image_width",
        "is_original",
        "is_screenshot",
        "is_flagged",
        "is_animated",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "verification",
        "rating",
        "is_original",
        "is_screenshot",
        "is_flagged",
        "is_animated",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "sample",
        "source",
        "source_id",
        "image_height",
        "image_width",
        "image_size",
        "sample_height",
        "sample_width",
        "sample_size",
        "color_dominant",
        "color_palette",
        "duration",
        "hash_md5",
        "hash_perceptual",
    )
    autocomplete_fields = ("tags", "characters")
    raw_id_fields = ("artist",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "is_nsfw")
    list_filter = ("is_nsfw",)
    search_fields = ("name", "description")
