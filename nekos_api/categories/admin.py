from django.contrib import admin

from .models import Category

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    """
    Admin page for categories.
    """

    list_display = (
        'name',
        'description',
        'is_nsfw',
        'created_at'
    )
    readonly_fields = ['id', 'created_at', 'updated_at']
    search_fields = (
        'name__icontains',
        'description__icontains'
    )
    list_filter = ['is_nsfw']


admin.site.register(Category, CategoryAdmin)