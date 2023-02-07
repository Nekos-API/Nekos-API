from django.contrib import admin

from .models import Image

# Register your models here.


class ImageAdmin(admin.ModelAdmin):
    """
    Images admin.
    """

    list_display = ('title', 'artist', 'updated_at', 'created_at')
    list_filter = ('is_original', 'is_verified', 'age_rating')
    raw_id_fields = ('artist',)
    filter_horizontal = ('characters', 'categories')
    readonly_fields = ('height', 'width', 'aspect_ratio', 'primary_color', 'dominant_color')


admin.site.register(Image, ImageAdmin)
