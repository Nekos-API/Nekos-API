from django.contrib import admin

from nekosapi.characters.models import Character


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "aliases",
        "ages",
        "height",
        "weight",
        "gender",
        "species",
        "birthday",
        "nationality",
        "occupations",
    )
    search_fields = (
        "name",
        "aliases",
        "gender",
        "species",
        "nationality",
        "occupations",
    )
    raw_id_fields = ("main_image",)
