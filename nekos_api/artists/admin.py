from django.contrib import admin

from .models import Artist

# Register your models here.


class ArtistAdmin(admin.ModelAdmin):
    list_display = ("name", "aliases", "links")
    readonly_fields = ("id",)
    search_fields = ("name__icontains", "aliases__icontains")


admin.site.register(Artist, ArtistAdmin)
