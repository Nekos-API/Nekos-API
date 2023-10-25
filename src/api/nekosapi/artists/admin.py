from django.contrib import admin

from nekosapi.artists.models import Artist


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ("name", "aliases", "policy_repost", "policy_credit", "policy_ai")
    list_filter = ("policy_repost", "policy_credit", "policy_ai")
    search_fields = ("name", "aliases", "links")
