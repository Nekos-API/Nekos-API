from django.contrib import admin

from .models import Image, ImageSourceResult

# Register your models here.


@admin.action(description="Mark selected images as verified")
def verify_images(modeladmin, request, queryset):
    queryset.update(verification_status=Image.VerificationStatus.VERIFIED)


@admin.action(description="Mark selected images as not reviewed")
def unverify_images(modeladmin, request, queryset):
    queryset.update(verification_status=Image.VerificationStatus.NOT_REVIEWED)


class ImageAdmin(admin.ModelAdmin):
    """
    Images admin.
    """

    list_display = (
        "title",
        "artist",
        "age_rating",
        "verification_status",
        "source_name",
        "created_at",
        "updated_at",
    )
    list_filter = ("is_original", "verification_status", "age_rating")
    raw_id_fields = ("artist",)
    filter_horizontal = ("characters", "categories")
    readonly_fields = (
        "height",
        "width",
        "aspect_ratio",
        "palette",
        "dominant_color",
        "mimetype",
        "file_size",
        "hash_perceptual",
    )
    search_fields = ("title", "uploader__username", "artist__name", "artist__aliases", "categories__name")
    autocomplete_fields = ("characters", "categories")
    actions = [verify_images, unverify_images]


class ImageSourceResultAdmin(admin.ModelAdmin):
    list_display = ("id", "image", "similarity", "status")
    list_filter = ("status",)
    raw_id_fields = ("image",)


admin.site.register(Image, ImageAdmin)
admin.site.register(ImageSourceResult, ImageSourceResultAdmin)
