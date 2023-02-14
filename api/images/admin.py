from django.contrib import admin

from .models import Image

# Register your models here.


@admin.action(description='Mark selected images as verified')
def verify_images(modeladmin, request, queryset):
    queryset.update(verification_status=Image.VerificationStatus.VERIFIED)


class ImageAdmin(admin.ModelAdmin):
    """
    Images admin.
    """

    list_display = ('title', 'artist', 'updated_at', 'created_at')
    list_filter = ('is_original', 'verification_status', 'age_rating')
    raw_id_fields = ('artist',)
    filter_horizontal = ('characters', 'categories')
    readonly_fields = ('height', 'width', 'aspect_ratio', 'primary_color', 'dominant_color')
    actions = [verify_images]


admin.site.register(Image, ImageAdmin)
