from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User, DiscordUser, GoogleUser, GitHubUser, Domain


class NekosUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (_("Library"), {"fields": ("liked_images", "saved_images")}),
    )
    fieldsets[0][1]["fields"] = fieldsets[0][1]["fields"] + ("avatar_image",)
    autocomplete_fields = ("liked_images", "saved_images")


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


class DomainAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "verified", "verification_method")
    raw_id_fields = ("user",)
    search_fields = ("name", "user__username")
    list_filter = ("verified", "verification_method")
    readonly_fields = ("verification_token",)


admin.site.register(User, NekosUserAdmin)
admin.site.register(DiscordUser, DiscordUserAdmin)
admin.site.register(GoogleUser, GoogleUserAdmin)
admin.site.register(GitHubUser, GitHubUserAdmin)
admin.site.register(Domain, DomainAdmin)
