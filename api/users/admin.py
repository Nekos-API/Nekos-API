from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User, DiscordUser, GoogleUser, GitHubUser


class NekosUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (_("Library"), {"fields": ("liked_images", "saved_images")}),
    )
    fieldsets[0][1]["fields"] = fieldsets[0][1]["fields"] + ("avatar_image",)


class DiscordUserAdmin(admin.ModelAdmin):
    list_display = ("user", "email", "id")
    raw_id_fields = ("user",)
    search_fields = ("user__username__icontains", "email__icontains")


class GoogleUserAdmin(admin.ModelAdmin):
    list_display = ("user", "email", "id")
    raw_id_fields = ("user",)
    search_fields = ("user__username__icontains", "email__icontains")


class GitHubUserAdmin(admin.ModelAdmin):
    list_display = ("user", "email", "id")
    raw_id_fields = ("user",)
    search_fields = ("user__username__icontains", "email__icontains")


admin.site.register(User, NekosUserAdmin)
admin.site.register(DiscordUser, DiscordUserAdmin)
admin.site.register(GoogleUser, GoogleUserAdmin)
admin.site.register(GitHubUser, GitHubUserAdmin)
