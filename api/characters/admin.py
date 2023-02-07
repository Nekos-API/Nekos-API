from django.contrib import admin

from .models import Character

# Register your models here.


class CharacterAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "ages", "nationality", "occupations")
    search_fields = (
        "first_name__icontains",
        "last_name__icontains",
        "aliases__icontains",
        "description__icontains",
        "occupations__icontains",
    )

    @admin.display()
    def name(self, instance):
        return str(instance)


admin.site.register(Character, CharacterAdmin)
